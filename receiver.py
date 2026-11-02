
import socket
from protocol import encode_packet, decode_packet
from simulator import simulate_packet

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(("127.0.0.1", 5005))

expected_seq_by_transfer = {}

print("Mini-TCP Go-Back-N Receiver started.")
print("Listening on 127.0.0.1:5005")

while True:
    packet_bytes, sender_address = receiver_socket.recvfrom(4096)

    try:
        packet = decode_packet(packet_bytes)

        if packet["type"] != "DATA":
            continue

        transfer_id = packet["transfer_id"]
        seq = packet["seq"]
        expected_seq = expected_seq_by_transfer.get(transfer_id, 0)

        if seq == expected_seq:
            print(f"\nReceived packet {seq}")
            print("Message:", packet["payload"].decode("utf-8"))

            expected_seq_by_transfer[transfer_id] = expected_seq + 1

        elif seq < expected_seq:
            print(f"Duplicate packet {seq}; ignoring payload.")

        else:
            print(
                f"Out-of-order packet {seq}; "
                f"expected {expected_seq}. Ignoring payload."
            )

        # ACK contains the next sequence number expected.
        ack_bytes = encode_packet(
            "ACK", transfer_id,
            expected_seq_by_transfer.get(transfer_id, 0),
            b""
        )

        dropped = simulate_packet("ACK")

        if dropped:
            print("[SIMULATOR] ACK lost.")
        else:
            receiver_socket.sendto(ack_bytes, sender_address)
            print(
                "Cumulative ACK sent:",
                expected_seq_by_transfer.get(transfer_id, 0)
            )

    except (ValueError, KeyError, UnicodeDecodeError) as error:
        print("Invalid packet:", error)