# mac_filter_ap.py
# extends standard_ap with MAC filter buffer and monitoring thread.
# detects DoS flooding by tracking auth requests per MAC.

from .standard_ap import standard_ap
from collections import defaultdict, deque


class mac_filter_ap(standard_ap):
    def __init__(self):
        super().__init__()
        self.mac_requests = defaultdict(deque)
        self.blacklist = set()
        self.window = 3000
        self.threshold = 5

    def receive(self, pkt, collided, timestamp):  # should be inside the class
        if collided:
            self.collisions += 1
            return

        if pkt.ptype != "auth_req":
            return

        mac = pkt.src_mac

        if mac in self.blacklist:
            return

        timestamps = self.mac_requests[mac]
        timestamps.append(timestamp)

        while timestamps and (timestamp - timestamps[0] > self.window):
            timestamps.popleft()

        if len(timestamps) > self.threshold:
            self.blacklist.add(mac)

        super().receive(pkt, collided, timestamp)