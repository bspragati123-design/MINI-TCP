
import socket

from protocol import encode_packet, decode_packet
from simulator import simulate_packet
from file_transfer_receiver import FileTransferReceiver

ADDRESS = ("127.0.0.1", 5005)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDRESS)

receiver = FileTransferReceiver()

print("Mini-TCP File Receiver started.")
print("Listening on 127.0.0.1:5005")

while True:
    packet_bytes, sender_address = sock.recvfrom(4096)

    try:
        packet = decode_packet(packet_bytes)

        if packet["type"] not in {"FILE_START", "DATA", "FILE_END"}:
            continue

        print(
            f"Received {packet['type']} "
            f"sequence {packet['seq']}"
        )

        result = receiver.process_packet(packet)

        if result is None:
            continue

        _, ack_seq = result

        ack_bytes = encode_packet(
            "ACK",
            packet["transfer_id"],
            ack_seq,
            b""
        )

        if simulate_packet("ACK"):
            print(f"Simulated loss of ACK {ack_seq}")
        else:
            sock.sendto(ack_bytes, sender_address)
            print(f"Sent cumulative ACK {ack_seq}")

    except (ValueError, KeyError, UnicodeDecodeError) as error:
        print("Invalid packet:", error)