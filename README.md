# Mini-TCP: Reliable File Transfer over UDP

A Python-based implementation of reliable file transfer over UDP using Go-Back-N sliding window protocol, acknowledgements, retransmissions, packet-loss simulation, and SHA-256 integrity verification.

## 1. Overview

UDP provides fast, connectionless communication but does not guarantee packet delivery, ordering, or retransmission.

Mini-TCP demonstrates how reliability mechanisms can be implemented on top of UDP. It uses concepts inspired by TCP to transfer files reliably, even when packet loss is simulated.

This is an educational Computer Networks project developed using Python.

## 2. Objectives

- Understand UDP socket programming.
- Implement a custom packet-based communication protocol.
- Apply the Go-Back-N sliding window mechanism.
- Handle packet loss using acknowledgements and retransmissions.
- Verify file integrity using SHA-256 hashing.
- Measure file-transfer performance under different network conditions.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| UDP Sockets | Network communication |
| JSON | Packet structure and serialization |
| Go-Back-N | Reliable data transmission |
| SHA-256 | File integrity verification |
| Base64 | Binary payload encoding |
| Git and GitHub | Version control |

## 4. Key Features

- **Custom packet protocol:** Uses packet types, sequence numbers, transfer IDs, payload lengths, and checksums.
- **Reliable transmission:** Uses Go-Back-N sliding window protocol.
- **Acknowledgements:** Uses cumulative acknowledgements to track received packets.
- **Retransmission:** Resends unacknowledged packets after timeout.
- **Network simulation:** Simulates packet loss and transmission delays.
- **File transfer:** Supports empty, small, and large files.
- **Integrity verification:** Uses SHA-256 to compare original and received files.
- **Performance monitoring:** Records transfer time, packets, retransmissions, simulated drops, timeouts, and throughput.

## 5. Project Structure

```text
MINI-TCP/
│
├── create_test_file.py
├── file_integrity.py
├── file_metadata.py
├── file_receiver.py
├── file_sender.py
├── file_transfer_receiver.py
├── file_utils.py
├── metrics.py
├── network_file_receiver.py
├── network_file_sender.py
├── protocol.py
├── receiver.py
├── sender.py
├── simulator.py
│
├── test_empty_file.py
├── test_file_metadata.py
├── test_file_receiver.py
├── test_file_sender.py
├── test_file_transfer_receiver.py
├── test_file_utils.py
├── test_integrity.py
├── test_invalid_packet.py
├── test_metrics.py
│
├── files/
│   ├── empty.txt
│   ├── large_sample.txt
│   ├── sample.txt
│   └── small.txt
│
├── received/
├── README.md
└── .gitignore
```

## 6. How It Works

The file-transfer process follows these stages:

1. **File preparation:** The sender reads the file and divides it into smaller chunks.
2. **Packet creation:** Each chunk is converted into a DATA packet with a sequence number and checksum.
3. **File initiation:** A FILE_START packet carries file metadata.
4. **Data transmission:** The sender transmits packets using a sliding window.
5. **Acknowledgement:** The receiver sends cumulative ACKs for successfully received packets.
6. **Retransmission:** Unacknowledged packets are retransmitted after a timeout.
7. **File reconstruction:** The receiver combines the received chunks in the correct order.
8. **File completion:** A FILE_END packet indicates completion of the transfer.
9. **Integrity verification:** SHA-256 hashes are compared to verify that the received file matches the original.

## 7. Running the Project

### Prerequisites

- Python 3 installed.
- Git installed.
- VS Code or another Python-compatible editor.

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project directory

```bash
cd Mini-TCP
```

### Step 3: Start the receiver

Open the first terminal:

```bash
python network_file_receiver.py
```

### Step 4: Start the sender

Open a second terminal:

```bash
python network_file_sender.py
```

The sender transfers the configured sample file to the receiver.

The received file is saved inside the `received/` directory.

**Current implementation:** The network sender and receiver use localhost (`127.0.0.1`). Therefore, the current configuration is intended for testing on the same computer.

## 8. Testing

The project has been tested with different file sizes and packet-loss conditions.

### File-transfer tests

| Test case | Result |
|---|---|
| Empty file | Passed |
| Small file | Passed |
| Large file | Passed |
| Invalid packet | Rejected successfully |
| File integrity verification | Passed |

### Packet-loss experiments

The large sample file (19,000 bytes) was transferred under three simulated packet-loss conditions.

| Metric | 5% Loss | 15% Loss | 30% Loss |
|---|---:|---:|---:|
| Transfer time (seconds) | 18.859 | 33.344 | 59.829 |
| Packets transmitted | 49 | 57 | 75 |
| Retransmissions | 11 | 26 | 48 |
| Network bytes sent | 40,818 | 45,823 | 61,591 |
| Simulated packet drops | 3 | 12 | 39 |
| Timeout events | 3 | 8 | 20 |
| Throughput (bytes/sec) | 1007.48 | 569.82 | 317.57 |
| SHA-256 verification | Passed | Passed | Passed |

*Note: Results are from individual simulation runs. Packet-loss outcomes and performance measurements may vary between runs.*

### Observation

As simulated packet loss increases:

- The number of retransmissions increases.
- Timeout events become more frequent.
- Transfer duration increases.
- Useful throughput decreases.

The matching SHA-256 hashes confirm that the original and received files were identical in the tested transfers.

## 9. Performance Metrics

Mini-TCP records the following metrics:

- Transfer time
- Number of packets transmitted
- Number of retransmissions
- Network bytes sent
- File bytes transferred
- Simulated packet drops
- Timeout events
- Useful throughput

These measurements help evaluate the effect of packet loss on reliable file transmission.

## 10. Limitations

- The current sender and receiver are configured for localhost communication.
- The project does not implement the complete TCP specification.
- Network conditions are simulated rather than measured from a real network.
- The current implementation is an educational prototype, not a production-ready file-transfer service.

## 11. Future Enhancements

- Support communication between two computers over a local network.
- Add command-line arguments for file selection.
- Allow configurable packet-loss and delay probabilities.
- Improve error handling and transfer recovery.
- Add a graphical user interface.
- Evaluate performance under real network conditions.

## 12. Conclusion

Mini-TCP demonstrates how reliable file transfer can be implemented over UDP using concepts such as Go-Back-N sliding window protocol, cumulative acknowledgements, retransmissions, and integrity verification.

The project provides practical experience with network programming, transport-layer reliability, file handling, and performance analysis using Python.

---

**Project:** Mini-TCP – Reliable File Transfer over UDP  
**Language:** Python  
**Domain:** Computer Networks