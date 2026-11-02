# Mini-TCP: Reliable File Transfer Protocol over UDP

## 1. Project Overview

Mini-TCP is an educational implementation of a reliable file transfer protocol built using Python and UDP sockets.

UDP provides fast communication but does not guarantee packet delivery, ordering, or retransmission. Mini-TCP addresses these limitations by implementing reliability mechanisms inspired by TCP.

The project demonstrates how reliable communication can be achieved over an unreliable network.

## 2. Problem Statement

UDP is a connectionless transport protocol that does not guarantee reliable data delivery. Packets may be lost, duplicated, or received out of order.

The objective of Mini-TCP is to design and implement a reliable file transfer mechanism over UDP using packet sequencing, acknowledgements, retransmissions, timeout handling, and data integrity verification.

## 3. Objectives

- Implement reliable communication using UDP sockets.
- Design a custom packet format.
- Implement Go-Back-N sliding window protocol.
- Detect packet corruption using checksums.
- Handle packet loss using acknowledgements and retransmissions.
- Support file transfer of different sizes.
- Verify transferred files using SHA-256.
- Analyze performance under different network conditions.

## 4. Technologies Used

- Programming Language: Python
- Networking: UDP sockets
- Protocol Design: Custom JSON-based packets
- Reliability: Go-Back-N ARQ
- Integrity Verification: SHA-256
- Development Environment: Visual Studio Code
- Operating System: Windows

## 5. Key Features

- Custom packet creation and validation.
- Sequence numbers and cumulative acknowledgements.
- Go-Back-N sliding window mechanism.
- Timeout-based retransmission.
- Simulated packet loss and network delay.
- File metadata exchange.
- File chunking and reconstruction.
- SHA-256 file integrity verification.
- Performance measurement and reporting.
- Empty, small, and large file support.

## 6. Project Structure

```text
MINI-TCP/
│
├── files/
├── received/
│
├── protocol.py
├── sender.py
├── receiver.py
├── network_file_sender.py
├── network_file_receiver.py
├── file_sender.py
├── file_receiver.py
├── file_transfer_receiver.py
├── file_utils.py
├── file_metadata.py
├── file_integrity.py
├── simulator.py
├── metrics.py
├── create_test_file.py
│
├── test_empty_file.py
├── test_invalid_packet.py
├── test_file_metadata.py
├── test_file_receiver.py
├── test_file_sender.py
├── test_file_transfer_receiver.py
├── test_file_utils.py
├── test_integrity.py
├── test_metrics.py
│
└── README.md
```

## 7. Working Mechanism

1. The sender reads the input file.
2. The file is divided into smaller chunks.
3. File metadata is sent using a FILE_START packet.
4. Data chunks are transmitted using DATA packets.
5. The receiver validates packets and sends cumulative ACKs.
6. Missing acknowledgements trigger timeout-based retransmissions.
7. FILE_END indicates completion of the transfer.
8. The receiver reconstructs and saves the file.
9. SHA-256 hashes are compared to verify file integrity.

## 8. Network Simulation

The simulator introduces artificial packet loss and delay to reproduce unreliable network conditions.

The project was tested using three packet-loss probabilities:

- 5%
- 15%
- 30%

## 9. Testing

The following tests were performed:

- Empty file transfer.
- Small file transfer.
- Large file transfer.
- Invalid packet rejection.
- Packet-loss simulation.
- Retransmission and timeout handling.
- SHA-256 file integrity verification.

## 10. Performance Analysis

Performance was evaluated using:

- Transfer duration.
- Number of packets transmitted.
- Retransmissions.
- Simulated packet drops.
- Timeout events.
- Network bytes sent.
- Useful throughput.

## 11. Limitations

- The implementation is an educational protocol, not a replacement for TCP.
- Communication is currently configured for a local network endpoint.
- Packet-loss and delay behavior are simulated.
- The implementation does not provide TCP-level congestion control.

## 12. Future Enhancements

- Support transfers between different computers.
- Add adaptive retransmission timeouts.
- Implement congestion control.
- Add selective acknowledgement mechanisms.
- Develop a graphical monitoring dashboard.

## 13. Conclusion

Mini-TCP demonstrates how reliability mechanisms can be implemented over UDP. Through sequencing, acknowledgements, retransmissions, sliding windows, packet validation, and file integrity checks, the project provides practical insight into reliable transport-layer communication.
