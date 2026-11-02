
from pathlib import Path

def save_received_file(chunks, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("wb") as file:
        for chunk in chunks:
            file.write(chunk)

    print("File saved to:", output_path)