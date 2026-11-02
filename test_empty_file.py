
from file_sender import prepare_file_packets

packets, total_chunks = prepare_file_packets(
    "files/empty.txt",
    "empty_test_001"
)

print("Total chunks:", total_chunks)
print("Total packets:", len(packets))
print("Packet sequences:", list(packets.keys()))

assert total_chunks == 0
assert len(packets) == 2
assert list(packets.keys()) == [0, 1]

print("Empty file packet generation test passed!")
