# packet.py
# defines the packet structure used throughout the simulation.
# every message sent between nodes and the AP is represented as a packet.

# valid packet types in our simulation
PACKET_TYPES = ["auth_req", "auth_resp", "mcs_command"]

class packet:
    def __init__(self, ptype, src_mac, dst_mac, timestamp, size=1):
        # ptype     : what kind of packet this is (see PACKET_TYPES above)
        # src_mac   : MAC address of whoever sent this
        # dst_mac   : MAC address of the intended recipient, or broadcast for mcs_command
        # timestamp : simulation time (in ms) when this packet was created
        # size      : packet size in bytes, used later when calculating air time from MCS

        if ptype not in PACKET_TYPES:
            raise ValueError(f"unknown packet type: {ptype}. must be one of {PACKET_TYPES}")

        self.ptype = ptype
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.timestamp = timestamp
        self.size = size

    def __repr__(self):
        return f"packet(type={self.ptype}, src={self.src_mac}, dst={self.dst_mac}, t={self.timestamp}ms)"
