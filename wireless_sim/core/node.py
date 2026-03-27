# node.py
# base class for any device in the simulation. clients and the attacker extend this.

import math
import random
from .packet import packet


class node:
    def __init__(self, mac, x, y, tx_range, mcs=1, send_rate=100, is_attacker=False, spoof_pool_size=10):
        # send_rate  : transmit once every N ticks
        # is_attacker: if true, spoofs MACs from a small pool on every auth_req
        self.mac = mac
        self.x = x
        self.y = y
        self.tx_range = tx_range
        # mcs (modulation and coding scheme) controls transmission speed.
        # higher mcs = more bits per symbol = shorter air time = smaller collision window.
        # starts at 1, AP can command it higher to address hidden terminal collisions.
        self.mcs = mcs
        self.send_rate = send_rate
        self.is_attacker = is_attacker
        # attackers rotate through a fixed pool of spoofed MACs rather than generating
        # a unique one per packet — this lets the filter accumulate counts and detect them
        self.spoof_pool = [self._random_mac() for _ in range(spoof_pool_size)] if is_attacker else []

    def can_hear(self, other):
        # two nodes that can't hear each other can't do CSMA carrier sense,
        # so they'll transmit simultaneously and collide at the AP (hidden terminal problem).
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance <= self.tx_range

    def make_packet(self, ptype, dst_mac, timestamp):
        # pick a random MAC from the spoof pool if attacker, otherwise use real MAC
        src = random.choice(self.spoof_pool) if self.is_attacker else self.mac
        size = max(1, 10 - self.mcs)
        return packet(ptype, src, dst_mac, timestamp, size)

    def step(self, clock):
        # called every tick by the simulation. returns a packet if this node
        # is ready to transmit, otherwise None.
        if clock % self.send_rate == 0:
            return self.make_packet("auth_req", "ap:00:00:00:00:00", clock)
        return None

    def _random_mac(self):
        # generate a random MAC to simulate spoofing
        return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

    def update_mcs(self, new_mcs):
        # clamp to 1-7, the valid index range for 802.11n MCS
        self.mcs = max(1, min(7, new_mcs))

    def __repr__(self):
        return f"node(mac={self.mac}, pos=({self.x},{self.y}), mcs={self.mcs})"
