# node.py
# base class for any device in the simulation. clients and the attacker extend this.

import math
import random
from .packet import packet


# 802.11 CSMA/CA timing constants, approximated in ticks
DIFS_TICKS = 3
CW_MIN     = 4    # minimum contention window size
CW_MAX     = 64   # maximum contention window size, doubles on each collision

# node states for the CSMA/CA state machine
IDLE         = "idle"
DIFS_WAIT    = "difs_wait"
BACKOFF      = "backoff"
TRANSMITTING = "transmitting"


class node:
    def __init__(self, mac, x, y, tx_range, mcs=1, send_rate=100, is_attacker=False, spoof_pool_size=10):
        # send_rate  : how often this node generates a new packet to send, every N ticks
        # is_attacker: if true, spoofs MACs from a fixed pool on every auth_req
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

        # CSMA/CA state machine
        self.state           = IDLE
        self.difs_counter    = 0
        self.backoff_counter = 0
        self.cw              = CW_MIN   # contention window, grows on collision
        self.pending_packet  = None     # packet waiting to be transmitted

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

    def step(self, clock, channel):
        # CSMA/CA state machine. called every tick by the simulation.
        # returns a (node, packet) tuple if ready to transmit, otherwise None.

        # generate a new packet if idle and it's time to send
        if self.state == IDLE:
            if clock % self.send_rate == 0:
                self.pending_packet = self.make_packet("auth_req", "aa:00:00:00:00:00", clock)
                self.state = DIFS_WAIT
                self.difs_counter = DIFS_TICKS
            return None

        if self.state == DIFS_WAIT:
            if channel.is_busy(self, clock):
                # channel became busy during DIFS — reset and wait again
                self.difs_counter = DIFS_TICKS
                return None
            self.difs_counter -= 1
            if self.difs_counter <= 0:
                # DIFS complete, draw a random backoff from the contention window
                self.backoff_counter = random.randint(0, self.cw)
                self.state = BACKOFF
            return None

        if self.state == BACKOFF:
            if channel.is_busy(self, clock):
                # freeze backoff counter while channel is busy — resume when free
                return None
            self.backoff_counter -= 1
            if self.backoff_counter <= 0:
                # backoff expired, transmit
                self.state = TRANSMITTING
                return (self, self.pending_packet)
            return None

        if self.state == TRANSMITTING:
            # simulation will call on_success or on_collision after processing
            return None

    def on_success(self):
        # reset state after a successful transmission
        self.cw = CW_MIN
        self.pending_packet = None
        self.state = IDLE

    def on_collision(self):
        # double the contention window on collision (exponential backoff),
        # then re-enter backoff with the new larger window.
        self.cw = min(self.cw * 2, CW_MAX)
        self.backoff_counter = random.randint(0, self.cw)
        self.state = BACKOFF

    def _random_mac(self):
        return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

    def update_mcs(self, new_mcs):
        # clamp to 1-7, the valid index range for 802.11n MCS
        self.mcs = max(1, min(7, new_mcs))

    def __repr__(self):
        return f"node(mac={self.mac}, pos=({self.x},{self.y}), mcs={self.mcs})"
