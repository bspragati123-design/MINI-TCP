import json
import base64
import hashlib


ALLOWED_TYPES = {"DATA", "ACK", "FILE_START", "FILE_END"}


def encode_packet(message_type, transfer_id, seq, payload):
    if message_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported message type")

    if not isinstance(transfer_id, str) or not transfer_id:
        raise ValueError("Transfer ID must be a non-empty string")

    if not isinstance(seq, int) or isinstance(seq, bool) or seq < 0:
        raise ValueError("Sequence number must be a non-negative integer")

    if not isinstance(payload, bytes):
        raise TypeError("Payload must be bytes")

    packet = {
        "type": message_type,
        "transfer_id": transfer_id,
        "seq": seq,
        "length": len(payload),
        "checksum": hashlib.sha256(payload).hexdigest(),
        "payload": base64.b64encode(payload).decode("ascii")
    }

    return json.dumps(packet).encode("utf-8")


def decode_packet(packet_bytes):
    packet = json.loads(packet_bytes.decode("utf-8"))

    required_fields = {
        "type", "transfer_id", "seq",
        "length", "checksum", "payload"
    }

    if not isinstance(packet, dict) or not required_fields.issubset(packet):
        raise ValueError("Missing packet fields")

    if packet["type"] not in ALLOWED_TYPES:
        raise ValueError("Unsupported message type")

    if not isinstance(packet["transfer_id"], str) or not packet["transfer_id"]:
        raise ValueError("Invalid transfer ID")

    if not isinstance(packet["seq"], int) or isinstance(packet["seq"], bool) or packet["seq"] < 0:
        raise ValueError("Invalid sequence number")

    if not isinstance(packet["length"], int) or isinstance(packet["length"], bool) or packet["length"] < 0:
        raise ValueError("Invalid payload length")

    if not isinstance(packet["checksum"], str):
        raise ValueError("Invalid checksum field")

    if not isinstance(packet["payload"], str):
        raise ValueError("Invalid payload field")

    payload = base64.b64decode(packet["payload"], validate=True)

    if len(payload) != packet["length"]:
        raise ValueError("Payload length mismatch")

    actual_checksum = hashlib.sha256(payload).hexdigest()

    if actual_checksum != packet["checksum"]:
        raise ValueError("Checksum mismatch")

    return {
        "type": packet["type"],
        "transfer_id": packet["transfer_id"],
        "seq": packet["seq"],
        "length": packet["length"],
        "checksum": packet["checksum"],
        "payload": payload
    }