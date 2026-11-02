
from file_utils import read_file_chunks
from file_metadata import create_file_metadata, parse_file_metadata

path = "files/sample.txt"
chunks = read_file_chunks(path)

metadata = create_file_metadata(path, len(chunks))
print("Encoded metadata:", metadata)

filename, total_chunks = parse_file_metadata(metadata)
print("Filename:", filename)
print("Total chunks:", total_chunks)