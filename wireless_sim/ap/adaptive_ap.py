# adaptive_ap.py
# extends mac_filter_ap with MCS control.
# handles both DoS detection and hidden terminal collisions simultaneously.

from .mac_filter_ap import mac_filter_ap


class adaptive_ap(mac_filter_ap):
   def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes
        self.collision_window = 3000
        self.collision_timestamps = []
        self.collision_threshold = 10

def receive(self, pkt, collided, timestamp):
        if collided:
            self.collision_timestamps.append(timestamp)

        # sliding window for collisions
        self.collision_timestamps = [
            t for t in self.collision_timestamps
            if timestamp - t <= self.collision_window
        ]

        if len(self.collision_timestamps) > self.collision_threshold:
            self._increase_mcs()
            self.collision_timestamps.clear()

        super().receive(pkt, collided, timestamp)

def _increase_mcs(self):
        for node in self.nodes:
            node.update_mcs(node.mcs + 1)
        # print("[MCS INCREASE]")