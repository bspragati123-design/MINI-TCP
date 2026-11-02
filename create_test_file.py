
from pathlib import Path

Path("files/large_sample.txt").write_bytes(
    (b"Mini-TCP reliable file transfer test.\n" * 500)
)

print("Large test file created.")
print("Size:", Path("files/large_sample.txt").stat().st_size, "bytes")