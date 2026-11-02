
from pathlib import Path

CHUNK_SIZE = 512

def read_file_chunks(file_path):
    file_path = Path(file_path)
    chunks = []

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            chunks.append(chunk)

    return chunks