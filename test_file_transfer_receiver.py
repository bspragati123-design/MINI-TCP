from file_sender import prepare_file_packets
from file_transfer_receiver import FileTransferReceiver
from protocol import decode_packet
from file_integrity import calculate_sha256

packets, _ = prepare_file_packets(
    "files/sample.txt", "local-test"
)

receiver = FileTransferReceiver()

for packet_bytes in packets.values():
    packet = decode_packet(packet_bytes)
    print("Processing:", packet["type"])
    print("Result:", receiver.process_packet(packet))

original_hash = calculate_sha256("files/sample.txt")
received_hash = calculate_sha256("received/sample.txt")

print("Files match:", original_hash == received_hash)