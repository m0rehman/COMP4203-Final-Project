# standard_ap.py
# a basic AP with no filtering or collision response.
# used as the control case in evaluation.

from .base_ap import base_ap


class standard_ap(base_ap):
    def receive(self, pkt, collided, timestamp):
        pass
