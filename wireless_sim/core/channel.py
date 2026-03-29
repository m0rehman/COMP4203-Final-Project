# core/channel.py
# models the wireless channel with CSMA/CA.
# tracks active transmissions and exposes channel state so nodes can
# perform carrier sense before transmitting.

from itertools import combinations

# 802.11 timing constants, approximated in ticks
DIFS_TICKS = 3   # distributed interframe space — minimum idle time before transmitting
SIFS_TICKS = 1   # short interframe space — used for ACK responses


class channel:
    def __init__(self):
        # active_transmissions: list of dicts tracking each ongoing transmission
        # each entry: {sender, packet, start, end}
        self.active_transmissions = []

    def is_busy(self, node, timestamp):
        # a node senses the channel as busy if any node it can hear is currently transmitting.
        # nodes that are out of range of each other won't sense each other's transmissions —
        # this is what causes the hidden terminal problem.
        self._clear_finished(timestamp)
        for tx in self.active_transmissions:
            if node.can_hear(tx["sender"]):
                return True
        return False

    def transmit(self, sender, pkt, timestamp):
        # add a new transmission to the channel.
        # duration is derived from packet size — larger size means longer air time.
        # higher MCS produces smaller packets (see node.make_packet), so they clear faster.
        duration = pkt.size
        self.active_transmissions.append({
            "sender": sender,
            "packet": pkt,
            "start": timestamp,
            "end": timestamp + duration
        })

    def process(self, timestamp):
        # check all transmissions that are finishing this tick for collisions.
        # two packets collide if their senders couldn't hear each other —
        # meaning neither could defer to the other via CSMA carrier sense.
        finishing = [tx for tx in self.active_transmissions if tx["end"] <= timestamp]
        self._clear_finished(timestamp)

        if len(finishing) <= 1:
            return [tx["packet"] for tx in finishing], []

        collided = set()
        for (tx_a, tx_b) in combinations(finishing, 2):
            if not tx_a["sender"].can_hear(tx_b["sender"]):
                collided.add(id(tx_a["packet"]))
                collided.add(id(tx_b["packet"]))

        successful = [tx["packet"] for tx in finishing if id(tx["packet"]) not in collided]
        failed     = [tx["packet"] for tx in finishing if id(tx["packet"]) in collided]

        return successful, failed

    def _clear_finished(self, timestamp):
        self.active_transmissions = [
            tx for tx in self.active_transmissions if tx["end"] > timestamp
        ]
