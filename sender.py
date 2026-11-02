
import socket
import uuid
import time
from protocol import encode_packet, decode_packet
from simulator import simulate_packet

receiver_address = ("127.0.0.1", 5005)

WINDOW_SIZE = 4
TIMEOUT_SECONDS = 2
MAX_RETRIES = 5

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.settimeout(0.2)

transfer_id = uuid.uuid4().hex
base = 0
next_seq = 0
packets = {}
messages = []

print("Mini-TCP Go-Back-N Sender")
print("Transfer ID:", transfer_id)
print("Enter messages; type 'send' to transmit them.")
print("Type 'exit' to quit.")

while True:
    message = input("Message: ")
    if message.lower() == "exit":
        break
    if message.lower() == "send":
        break
    if message:
        messages.append(message.encode("utf-8"))

if not messages:
    print("No messages to send.")
    sender_socket.close()
    raise SystemExit

for payload in messages:
    packets[next_seq] = encode_packet(
        "DATA", transfer_id, next_seq, payload
    )
    next_seq += 1

next_to_send = 0
base = 0
next_seq = 0
retries = 0
last_send_time = time.monotonic()

while base < len(packets):
    # Send new packets while the window has space.
    while next_to_send < len(packets) and (
        next_to_send < base + WINDOW_SIZE
    ):
        dropped = simulate_packet("DATA")
        if dropped:
            print(f"Simulated loss of DATA {next_to_send}")
        else:
            sender_socket.sendto(
                packets[next_to_send], receiver_address
            )
            print(f"Sent DATA {next_to_send}")

        if base == next_to_send:
            last_send_time = time.monotonic()

        next_to_send += 1

    try:
        ack_bytes, ack_address = sender_socket.recvfrom(4096)

        if ack_address != receiver_address:
            continue

        ack = decode_packet(ack_bytes)

        if (ack["type"] == "ACK"
                and ack["transfer_id"] == transfer_id):
            ack_next = ack["seq"]

            if base < ack_next <= next_to_send:
                print(f"Cumulative ACK received: {ack_next}")
                base = ack_next
                retries = 0
                last_send_time = time.monotonic()

    except socket.timeout:
        if time.monotonic() - last_send_time >= TIMEOUT_SECONDS:
            if retries >= MAX_RETRIES:
                print("Transfer failed: retry limit reached.")
                break

            retries += 1
            print(
                f"Timeout. Go-Back-N retransmission "
                f"({retries}/{MAX_RETRIES})"
            )

            # Retransmit every outstanding packet.
            for seq in range(base, next_to_send):
                dropped = simulate_packet("DATA")
                if dropped:
                    print(f"Simulated loss of DATA {seq}")
                else:
                    sender_socket.sendto(
                        packets[seq], receiver_address
                    )
                    print(f"Retransmitted DATA {seq}")

            last_send_time = time.monotonic()

    except (ValueError, KeyError) as error:
        print("Invalid ACK:", error)

if base == len(packets):
    print("All messages acknowledged successfully.")

sender_socket.close()
print("Sender stopped.")