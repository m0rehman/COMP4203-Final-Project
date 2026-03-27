# packet.py
# defines the packet structure used throughout the simulation.
# every message sent between nodes and the AP is represented as a packet.


import uuid  #to generate a unique packet ID
import re #to validate MAC address format


PACKET_TYPES = ["auth_req", "auth_resp", "mcs_command"]
BROADCAST_MAC = "FF:FF:FF:FF:FF:FF"
MAC_REGEX = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"

class packet:
    def __init__(self, ptype, src_mac, dst_mac, timestamp, size=1, payload=None):

        # ptype     : what kind of packet this is (see PACKET_TYPES above)
        # src_mac   : MAC address of whoever sent this
        # dst_mac   : MAC address of the intended recipient, or broadcast for mcs_command
        # timestamp : simulation time (in ms) when this packet was created
        # size      : packet size in bytes, used later when calculating air time from MCS

        if ptype not in PACKET_TYPES:
            raise ValueError(f"unknown packet type: {ptype}. must be one of {PACKET_TYPES}")

        if not re.match(MAC_REGEX, src_mac):
            raise ValueError(f"invalid src_mac: {src_mac}")

        if dst_mac != BROADCAST_MAC and not re.match(MAC_REGEX, dst_mac):
            raise ValueError(f"invalid dst_mac: {dst_mac}")

        self.id = uuid.uuid4()
        self.ptype = ptype
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.timestamp = timestamp
        self.size = size
        self.payload = payload

    def __repr__(self):
        return f"packet(id={self.id}, type={self.ptype}, src={self.src_mac}, dst={self.dst_mac}, t={self.timestamp}ms)"

    def is_auth_request(self):
        return self.ptype == "auth_req"

    def is_auth_response(self):
        return self.ptype == "auth_resp"

    def is_mcs_command(self):
        return self.ptype == "mcs_command"
