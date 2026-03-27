# standard_ap.py
# a basic AP with no filtering or collision response.
# used as the control case in evaluation.

from .base_ap import base_ap

BUFFER_MAX = 50

class standard_ap(base_ap):
    def __init__(self, mac="ap:00:00:00:00:00"):
        super().__init__(mac)
        self.received = 0
        self.collisions = 0
        self.blocked_auths = 0
        self.unassociated_buffer = {}

    def receive(self, pkt, collided, timestamp):
        if collided:
            self.collisions += 1
            return

        if pkt.ptype != "auth_req":
            return

        if len(self.unassociated_buffer) >= BUFFER_MAX:
            self.blocked_auths += 1
            return

        self.unassociated_buffer[pkt.src_mac] = timestamp
        self.received += 1

    def stats(self):
            return {
                "received": self.received,
                "collisions": self.collisions,
                "blocked_auths": self.blocked_auths,
                "buffer_usage": len(self.unassociated_buffer)
            }
