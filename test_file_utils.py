
from file_utils import read_file_chunks

chunks = read_file_chunks("files/sample.txt")

print("Number of chunks:", len(chunks))
print("Total bytes:", sum(len(chunk) for chunk in chunks))
print("First chunk:", chunks[0].decode("utf-8"))