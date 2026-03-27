# standard_ap.py
# a basic AP with no filtering or MCS control.
# models the unassociated buffer filling up under attack, used as the control case.

from .base_ap import base_ap

BUFFER_MAX = 50  # max number of pending auth requests the AP can hold

class standard_ap(base_ap):
    def __init__(self):
        super().__init__()
        # unassociated buffer: holds MACs that have sent auth requests
        # but haven't completed the handshake yet
        # in a real AP this is bounded by memory, here we cap it at BUFFER_MAX
        self.unassociated_buffer = {}
        
        # metrics
        self.successful_auths = 0
        self.blocked_auths = 0
        self.total_collisions = 0

    def receive(self, pkt, collided, timestamp):
        if collided:
            self.total_collisions += 1
            return

        if pkt.ptype != "auth_req":
            return

        # if the buffer is full, the AP has no memory left to handle new requests —
        # legitimate users get blocked just like the attacker intended
        if len(self.unassociated_buffer) >= BUFFER_MAX:
            self.blocked_auths += 1
            return

        # log the request and count it as a successful auth
        self.unassociated_buffer[pkt.src_mac] = timestamp
        self.successful_auths += 1

    def stats(self):
        return {
            "successful_auths": self.successful_auths,
            "blocked_auths": self.blocked_auths,
            "total_collisions": self.total_collisions,
            "buffer_usage": len(self.unassociated_buffer)
        }
