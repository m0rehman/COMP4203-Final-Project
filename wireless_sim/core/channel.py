# channel.py
# models the wireless channel. given a list of simultaneous transmissions,
# determines which packets collide and which get through cleanly.

from itertools import combinations


class channel:
    def process(self, transmissions):
        # transmissions: list of (sender_node, packet) tuples sent in the same time slot.
        # returns (successful, collided) — both are lists of packets.

        if len(transmissions) <= 1:
            # nothing to collide with
            return [p for _, p in transmissions], []

        collided = set()

        # check every pair of senders. if two nodes can't hear each other,
        # they had no way to detect the channel was busy before transmitting,
        # so their packets collide at the AP.
        for (node_a, pkt_a), (node_b, pkt_b) in combinations(transmissions, 2):
            if not node_a.can_hear(node_b):
                collided.add(id(pkt_a))
                collided.add(id(pkt_b))

        successful = [p for _, p in transmissions if id(p) not in collided]
        failed     = [p for _, p in transmissions if id(p) in collided]

        return successful, failed
