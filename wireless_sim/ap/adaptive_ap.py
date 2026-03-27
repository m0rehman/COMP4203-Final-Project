# adaptive_ap.py
# extends mac_filter_ap with AP-controlled MCS.
# monitors collision rate and commands all nodes to increase MCS when collisions are high,
# inducing the short packet effect to reduce transmission overlap.

from .mac_filter_ap import mac_filter_ap

COLLISION_THRESHOLD = 0.30  # if more than 30% of packets in a window are collisions, increase MCS

class adaptive_ap(mac_filter_ap):
    def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes  # reference to all nodes so we can broadcast MCS commands
        self.window_packets = 0
        self.window_collisions = 0

    def receive(self, pkt, collided, timestamp):
        self.window_packets += 1
        if collided:
            self.window_collisions += 1

        # check collision rate every monitoring interval
        if timestamp - self.last_monitor_time >= 3000:
            self._check_collision_rate(timestamp)

        super().receive(pkt, collided, timestamp)

    def _check_collision_rate(self, timestamp):
        if self.window_packets == 0:
            return

        collision_rate = self.window_collisions / self.window_packets
        if collision_rate > COLLISION_THRESHOLD:
            self._broadcast_mcs_increase()

        # reset window counters
        self.window_packets = 0
        self.window_collisions = 0

    def _broadcast_mcs_increase(self):
        # command all nodes to step up their MCS by 1.
        # this is the AP-controlled short packet effect from the Tamai paper.
        for node in self.nodes:
            node.update_mcs(node.mcs + 1)

    def stats(self):
        s = super().stats()
        s.update({
            "current_mcs": self.nodes[0].mcs if self.nodes else 1
        })
        return s
