import random
import time

# Probability of dropping a packet: 30%
LOSS_PROBABILITY = 0.30

# Maximum artificial delay: 0.5 seconds
MAX_DELAY_SECONDS = 0.5


def simulate_packet(packet_type):
    # Randomly decide whether to drop this packet
    if random.random() < LOSS_PROBABILITY:
        print(f"[SIMULATOR] Dropped {packet_type} packet.")
        return True

    # Add a random delay
    delay = random.uniform(0, MAX_DELAY_SECONDS)

    if delay > 0.05:
        print(
            f"[SIMULATOR] Delaying {packet_type} "
            f"by {delay:.2f} seconds."
        )
        time.sleep(delay)

    return False