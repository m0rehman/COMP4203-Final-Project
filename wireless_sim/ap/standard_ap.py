# standard_ap.py
# a basic AP with no filtering or collision response.
# used as the control case in evaluation.

from .base_ap import base_ap


class standard_ap(base_ap):
    def __init__(self, mac="ap:00:00:00:00:00"):
        super().__init__(mac)
        self.received = 0      # count of successfully received packets
        self.collisions = 0    # count of collided packets

    def receive(self, pkt, collided, timestamp):
        # update counters
        if collided:
            self.collisions += 1
        else:
            self.received += 1

