
from protocol import decode_packet

invalid_packet = b"This is not a valid JSON packet"

try:
    decode_packet(invalid_packet)
    print("Test failed: Invalid packet was accepted.")

except (ValueError, KeyError, TypeError) as error:
    print("Invalid packet rejected successfully.")
    print("Error:", error)
