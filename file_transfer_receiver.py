
from file_metadata import parse_file_metadata
from file_receiver import save_received_file


class FileTransferReceiver:
    def __init__(self, output_dir="received"):
        self.output_dir = output_dir
        self.transfers = {}
        self.completed = {}

    def process_packet(self, packet):
        transfer_id = packet["transfer_id"]
        seq = packet["seq"]
        packet_type = packet["type"]

        # Re-ACK duplicate FILE_END packets.
        if packet_type == "FILE_END":
            if transfer_id in self.completed:
                return "ACK", seq + 1

        if packet_type == "FILE_START":
            # Re-ACK a repeated FILE_START.
            if transfer_id in self.transfers:
                return "ACK", 1

            filename, total_chunks = parse_file_metadata(
                packet["payload"]
            )

            self.transfers[transfer_id] = {
                "filename": filename,
                "total_chunks": total_chunks,
                "expected_seq": 1,
                "chunks": []
            }

            return "ACK", 1

        if transfer_id not in self.transfers:
            return None

        transfer = self.transfers[transfer_id]

        if packet_type == "DATA":
            expected = transfer["expected_seq"]

            if seq == expected:
                transfer["chunks"].append(packet["payload"])
                transfer["expected_seq"] += 1

            # ACK always indicates the next expected sequence.
            return "ACK", transfer["expected_seq"]

        if packet_type == "FILE_END":
            if transfer["expected_seq"] != transfer["total_chunks"] + 1:
                return "ACK", transfer["expected_seq"]

            output_path = (
                f"{self.output_dir}/{transfer['filename']}"
            )

            save_received_file(
                transfer["chunks"], output_path
            )

            self.completed[transfer_id] = True
            del self.transfers[transfer_id]

            return "ACK", seq + 1

        return None