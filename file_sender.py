
from file_utils import read_file_chunks
from file_metadata import create_file_metadata
from protocol import encode_packet

def prepare_file_packets(file_path, transfer_id):
    chunks = read_file_chunks(file_path)

    start_payload = create_file_metadata(
        file_path, len(chunks)
    )

    packets = {
        0: encode_packet(
            "FILE_START", transfer_id, 0, start_payload
        )
    }

    for seq, chunk in enumerate(chunks, start=1):
        packets[seq] = encode_packet(
            "DATA", transfer_id, seq, chunk
        )

    end_seq = len(chunks) + 1

    packets[end_seq] = encode_packet(
        "FILE_END", transfer_id, end_seq, b""
    )

    return packets, len(chunks)