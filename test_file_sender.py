
from file_sender import prepare_file_packets
from protocol import decode_packet

packets, total_chunks = prepare_file_packets(
    "files/sample.txt", "test-transfer"
)

print("Total chunks:", total_chunks)

for seq, packet_bytes in packets.items():
    packet = decode_packet(packet_bytes)
    print("Sequence:", seq, "Type:", packet["type"])