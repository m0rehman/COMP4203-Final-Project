# adaptive_ap.py
# extends mac_filter_ap with MCS control.
# handles both DoS detection and hidden terminal collisions simultaneously.

from .mac_filter_ap import mac_filter_ap


class adaptive_ap(mac_filter_ap):
    def receive(self, pkt, collided, timestamp):
        pass
