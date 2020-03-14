"""The Simple timer."""
import time


class STimer:
    """The simple timer class."""

    def __init__(self, duration):
        """Initializer."""
        self.start = self.timestamp()
        self.duration = duration

    @classmethod
    def timestamp(cls):
        """Current time stamp."""
        return int(time.time())

    def is_stop(self):
        """Check."""
        return self.timestamp() - self.start >= self.duration

    def sleep(self, nsecond=0):
        """Sleep."""
        time.sleep(nsecond)
