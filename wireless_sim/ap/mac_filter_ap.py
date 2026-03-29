# extends standard_ap with a MAC filter buffer and sliding window monitor.
# detects DoS flooding by tracking auth request frequency per MAC.

from .standard_ap import standard_ap
from collections import defaultdict, deque


class mac_filter_ap(standard_ap):
    def __init__(self):
        super().__init__()
        self.mac_requests = defaultdict(deque)
        self.blacklist = set()
        self.window = 3000
        self.threshold = 20
        self.first_attack_time = None
        self.detection_latency = None

    def receive(self, pkt, collided, timestamp):
        # collisions and non-auth packets are handled entirely by standard_ap
        if collided or pkt.ptype != "auth_req":
            super().receive(pkt, collided, timestamp)
            return

        mac = pkt.src_mac

        # drop and count packets from already-blacklisted MACs
        if mac in self.blacklist:
            self.total_packets += 1
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

        # pass to standard_ap for buffer logic and counting
        super().receive(pkt, collided, timestamp)

    def stats(self):
        s = super().stats()
        s.update({
            "blacklisted_macs": len(self.blacklist),
            "detection_latency_ms": self.detection_latency
        })
        return s
