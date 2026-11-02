from metrics import TransferMetrics
import socket
import uuid
import time
import os

from file_sender import prepare_file_packets
from protocol import decode_packet
from simulator import simulate_packet

RECEIVER_ADDRESS = ("127.0.0.1", 5005)
WINDOW_SIZE = 4
TIMEOUT_SECONDS = 2
MAX_RETRIES = 5


def send_file_packets(file_path):
    transfer_id = uuid.uuid4().hex
    metrics = TransferMetrics()
    metrics.record_file_size(os.path.getsize(file_path))
    packets, total_chunks = prepare_file_packets(
        file_path, transfer_id
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)

    base = 0
    next_to_send = 0
    retries = 0
    last_send_time = time.monotonic()
    total_packets = len(packets)

    print("Transfer ID:", transfer_id)
    print("Total chunks:", total_chunks)
    print("Total packets:", total_packets)

    while base < total_packets:

        while (next_to_send < total_packets
               and next_to_send < base + WINDOW_SIZE):

            if simulate_packet("DATA"):
                metrics.record_drop()
                print(f"Simulated loss of packet {next_to_send}")
            else:
                sock.sendto(packets[next_to_send], RECEIVER_ADDRESS)
                metrics.record_packet(len(packets[next_to_send]))
                print(f"Sent packet {next_to_send}")
            if base == next_to_send:
                last_send_time = time.monotonic()

            next_to_send += 1

        try:
            ack_bytes, ack_address = sock.recvfrom(4096)

            if ack_address != RECEIVER_ADDRESS:
                continue

            ack = decode_packet(ack_bytes)

            if (ack["type"] == "ACK"
                    and ack["transfer_id"] == transfer_id):
                ack_seq = ack["seq"]

                if base < ack_seq <= next_to_send:
                    print(f"Cumulative ACK received: {ack_seq}")
                    base = ack_seq
                    retries = 0
                    last_send_time = time.monotonic()

        except socket.timeout:
            if time.monotonic() - last_send_time >= TIMEOUT_SECONDS:
                if retries >= MAX_RETRIES:
                    print("Transfer failed: retry limit reached.")
                    sock.close()
                    return False

                retries += 1
                metrics.record_timeout()
                print(
                    f"Timeout: retransmitting outstanding packets "
                    f"({retries}/{MAX_RETRIES})"
                )

                for seq in range(base, next_to_send):
                    if simulate_packet("DATA"):
                        metrics.record_drop()
                        print(f"Simulated loss of packet {seq}")
                    else:
                        sock.sendto(packets[seq], RECEIVER_ADDRESS)
                        metrics.record_packet(len(packets[seq]), retransmission=True)
                        print(f"Retransmitted packet {seq}")

                last_send_time = time.monotonic()

        except (ValueError, KeyError) as error:
            print("Invalid ACK:", error)

    sock.close()
    print("All file packets acknowledged.")
    metrics.report()
    return True


if __name__ == "__main__":
    send_file_packets("files/sample.txt")