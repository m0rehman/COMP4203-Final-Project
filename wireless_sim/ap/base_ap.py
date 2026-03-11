# base_ap.py
# the simplest possible AP. receives packets and does nothing with them.
# all other AP variants extend this.

class base_ap:
    def __init__(self, mac="ap:00:00:00:00:00"):
        self.mac = mac

    def receive(self, pkt, collided, timestamp):
        # override this in subclasses to add filtering, monitoring, etc.
        pass
