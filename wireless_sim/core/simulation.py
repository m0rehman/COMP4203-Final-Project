# drives the simulation. each tick, runs the CSMA/CA state machine for legitimate nodes,
# delivers attacker packets directly to the AP (bypassing CSMA/CA),
# and processes channel collisions.

from .channel import channel
from .node import AP_MAC


class simulation:
    def __init__(self, nodes, ap, duration_ms, tick_ms=1):
        self.nodes = nodes
        self.ap = ap
        self.channel = channel()
        self.duration_ms = duration_ms
        self.tick_ms = tick_ms
        self.clock = 0
        # persistent map of packet id to sender — lives for the duration of each
        # transmission since packets stay in the channel for multiple ticks.
        self.sender_map = {}

    def run(self):
        while self.clock < self.duration_ms:
            self._tick()
            self.clock += self.tick_ms

    def _tick(self):
        # attacker traffic bypasses CSMA/CA entirely. in real 802.11, DoS flooding
        # uses management frames that don't respect normal channel access
        # delivering directly to the AP models this, and prevents the attacker from suppressing
        # legitimate traffic via carrier sense.
        for n in self.nodes:
            if n.is_attacker and self.clock % n.send_rate == 0:
                pkt = n.make_packet("auth_req", AP_MAC, self.clock)
                self.ap.receive(pkt, collided=False, timestamp=self.clock)

        # legitimate nodes go through CSMA/CA and the channel
        for n in self.nodes:
            if n.is_attacker:
                continue
            result = n.step(self.clock, self.channel)
            if result is not None:
                node, pkt = result
                self.channel.transmit(node, pkt, self.clock)
                self.sender_map[id(pkt)] = node

        # process the channel 
        # collisions only happen between legitimate nodes
        successful, collided = self.channel.process(self.clock)

        for pkt in successful:
            sender = self.sender_map.pop(id(pkt), None)
            if sender:
                sender.on_success()
            self.ap.receive(pkt, collided=False, timestamp=self.clock)

        for pkt in collided:
            sender = self.sender_map.pop(id(pkt), None)
            if sender:
                sender.on_collision()
            self.ap.receive(pkt, collided=True, timestamp=self.clock)
