# a basic AP with no filtering or MCS control.
# models the unassociated buffer filling up under attack, used as the control case.

from .base_ap import base_ap

BUFFER_MAX = 50


class standard_ap(base_ap):
    def __init__(self):
        super().__init__()
        # unassociated buffer 
        # holds MACs that have sent auth requess but haven't completed the handshake yet
        # in a real AP this is bounded by memory; here we cap it at BUFFER_MAX
        self.unassociated_buffer = {}
        self.received = 0
        self.collisions = 0
        self.blocked_auths = 0
        self.total_packets = 0

    def receive(self, pkt, collided, timestamp):
        self.total_packets += 1

        if collided:
            self.collisions += 1
            return

        if pkt.ptype != "auth_req":
            return

        # if the buffer is full, the AP has no memory left to handle new requests —
        # legitimate users get blocked just like the attacker intended
        if len(self.unassociated_buffer) >= BUFFER_MAX:
            self.blocked_auths += 1
            return

        self.unassociated_buffer[pkt.src_mac] = timestamp
        self.received += 1

    def stats(self):
        return {
            "total_packets": self.total_packets,
            "received": self.received,
            "collisions": self.collisions,
            "blocked_auths": self.blocked_auths,
            "buffer_usage": len(self.unassociated_buffer)
        }
