# mac_filter_ap.py
# extends standard_ap with a MAC filter buffer and sliding window monitor.
# detects DoS flooding by tracking auth request frequency per MAC.

from .standard_ap import standard_ap
from collections import defaultdict, deque


class mac_filter_ap(standard_ap):
    def __init__(self):
        super().__init__()
        self.mac_requests = defaultdict(deque)
        self.blacklist = set()
        self.window = 3000      # sliding window size in ms
        self.threshold = 5      # max auth requests allowed per MAC per window
        self.first_attack_time = None
        self.detection_latency = None

    def receive(self, pkt, collided, timestamp):
        if collided:
            self.collisions += 1
            return

        if pkt.ptype != "auth_req":
            return

        mac = pkt.src_mac

        if mac in self.blacklist:
            self.blocked_auths += 1
            return

        timestamps = self.mac_requests[mac]
        timestamps.append(timestamp)

        if self.first_attack_time is None and len(timestamps) == 1:
            self.first_attack_time = timestamp

        # evict timestamps outside the current window
        while timestamps and (timestamp - timestamps[0] > self.window):
            timestamps.popleft()

        if len(timestamps) > self.threshold:
            self.blacklist.add(mac)
            if self.detection_latency is None:
                self.detection_latency = timestamp - self.first_attack_time

        super().receive(pkt, collided, timestamp)

    def stats(self):
        return {
            "received": self.received,
            "collisions": self.collisions,
            "blocked_auths": self.blocked_auths,
            "blacklisted_macs": len(self.blacklist),
            "buffer_usage": len(self.unassociated_buffer),
            "detection_latency_ms": self.detection_latency
        }
