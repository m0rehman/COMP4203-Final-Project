# simulation.py
# drives the simulation. each tick, collects transmissions from all nodes,
# runs them through the channel, and delivers results to the AP.

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

    def run(self):
        while self.clock < self.duration_ms:
            self._tick()
            self.clock += self.tick_ms

    def _tick(self):
        # ask each node if it wants to transmit this tick.
        # nodes return a packet if they're ready to send, or None if not.
        transmissions = []
        for n in self.nodes:
            pkt = n.step(self.clock)
            if pkt is not None:
                transmissions.append((n, pkt))

        # let the channel sort out collisions
        successful, collided = self.channel.process(transmissions)

        # deliver results to the AP
        for pkt in successful:
            self.ap.receive(pkt, collided=False, timestamp=self.clock)
        for pkt in collided:
            self.ap.receive(pkt, collided=True, timestamp=self.clock)
