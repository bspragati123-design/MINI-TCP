
from file_utils import read_file_chunks
from file_receiver import save_received_file
from file_integrity import calculate_sha256

chunks = read_file_chunks("files/sample.txt")
save_received_file(chunks, "received/sample.txt")

original_hash = calculate_sha256("files/sample.txt")
received_hash = calculate_sha256("received/sample.txt")

print("Original SHA-256:", original_hash)
print("Received SHA-256:", received_hash)
print("Files match:", original_hash == received_hash)