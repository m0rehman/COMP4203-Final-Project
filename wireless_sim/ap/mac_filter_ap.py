# mac_filter_ap.py
# extends standard_ap with MAC filter buffer and monitoring thread.
# detects DoS flooding by tracking auth requests per MAC.

from .standard_ap import standard_ap


class mac_filter_ap(standard_ap):
    def receive(self, pkt, collided, timestamp):
        pass
