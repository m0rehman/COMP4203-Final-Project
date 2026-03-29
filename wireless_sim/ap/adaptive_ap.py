# extends mac_filter_ap with AP-controlled MCS.
# monitors collision rate and commands nodes to increase MCS when collisions spike,
# inducing the short packet effect to reduce transmission overlap.

from .mac_filter_ap import mac_filter_ap


class adaptive_ap(mac_filter_ap):
    def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes
        self.collision_window = 3000    # sliding window size in ms
        self.collision_threshold = 5    # collisions in window before MCS increase
        self.collision_timestamps = []
        self.mcs_increases = 0

    def receive(self, pkt, collided, timestamp):
        if collided:
            self.collision_timestamps.append(timestamp)

        # evict timestamps outside the current window
        self.collision_timestamps = [
            t for t in self.collision_timestamps
            if timestamp - t <= self.collision_window
        ]

        if len(self.collision_timestamps) > self.collision_threshold:
            self._increase_mcs()
            self.collision_timestamps.clear()

        super().receive(pkt, collided, timestamp)

    def _increase_mcs(self):
        # command all nodes to use a higher MCS 
        # shorter air time, fewer collisions
        for node in self.nodes:
            node.update_mcs(node.mcs + 1)
        self.mcs_increases += 1

    def stats(self):
        s = super().stats()
        s.update({
            "mcs_increases": self.mcs_increases,
            "current_mcs": self.nodes[0].mcs if self.nodes else 1
        })
        return s
