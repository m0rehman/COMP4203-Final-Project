# simulation.py
# drives the simulation. each tick, runs the CSMA/CA state machine for each node,
# registers transmissions on the channel, and delivers results to the AP.

from .channel import channel


class simulation:
    def __init__(self, nodes, ap, duration_ms, tick_ms=1):
        # duration_ms : how long to run the simulation
        # tick_ms     : time resolution, default 1ms per tick
        self.nodes = nodes
        self.ap = ap
        self.channel = channel()
        self.duration_ms = duration_ms
        self.tick_ms = tick_ms
        self.clock = 0
        # persistent map of packet id to sender, lives for the duration of each transmission.
        # rebuilt each tick won't work since packets stay in the channel for multiple ticks.
        self.sender_map = {}

    def run(self):
        while self.clock < self.duration_ms:
            self._tick()
            self.clock += self.tick_ms

    def _tick(self):
        # run the CSMA/CA state machine for each node.
        # nodes that are ready to transmit return a (node, packet) tuple.
        for n in self.nodes:
            result = n.step(self.clock, self.channel)
            if result is not None:
                node, pkt = result
                self.channel.transmit(node, pkt, self.clock)
                # register in persistent map so we can find the sender when packet finishes
                self.sender_map[id(pkt)] = node

        # process the channel — get back successful and collided packets
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
