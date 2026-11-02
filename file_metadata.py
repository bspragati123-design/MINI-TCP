
import json
from pathlib import Path

def create_file_metadata(file_path, total_chunks):
    return json.dumps({
        "filename": Path(file_path).name,
        "total_chunks": total_chunks
    }).encode("utf-8")

def parse_file_metadata(payload):
    metadata = json.loads(payload.decode("utf-8"))

    filename = metadata["filename"]
    total_chunks = metadata["total_chunks"]

    if not isinstance(filename, str) or not filename:
        raise ValueError("Invalid filename")

    if Path(filename).name != filename or filename in {".", ".."}:
        raise ValueError("Invalid filename")

    if (not isinstance(total_chunks, int)
            or isinstance(total_chunks, bool)
            or total_chunks < 0):
        raise ValueError("Invalid chunk count")

    return filename, total_chunks