
import time


class TransferMetrics:
    def __init__(self):
        self.start_time = time.monotonic()
        self.packets_sent = 0
        self.retransmissions = 0
        self.network_bytes_sent = 0
        self.file_bytes = 0
        self.simulated_drops = 0
        self.timeouts = 0

    def record_packet(self, packet_size, retransmission=False):
        self.packets_sent += 1
        self.network_bytes_sent += packet_size

        if retransmission:
            self.retransmissions += 1

    def record_file_size(self, size):
        self.file_bytes = size

    def record_drop(self):
        self.simulated_drops += 1

    def record_timeout(self):
        self.timeouts += 1

    def report(self):
        elapsed = max(time.monotonic() - self.start_time, 0.000001)
        throughput = self.file_bytes / elapsed

        print("\n--- Mini-TCP Performance Report ---")
        print(f"Transfer time: {elapsed:.3f} seconds")
        print(f"Packets transmitted: {self.packets_sent}")
        print(f"Retransmissions: {self.retransmissions}")
        print(f"Network bytes sent: {self.network_bytes_sent}")
        print(f"File bytes transferred: {self.file_bytes}")
        print(f"Simulated packet drops: {self.simulated_drops}")
        print(f"Timeout events: {self.timeouts}")
        print(f"Useful throughput: {throughput:.2f} bytes/second")
