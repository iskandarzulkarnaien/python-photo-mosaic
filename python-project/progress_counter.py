import sys

class ProgressCounter:
    def __init__(self, total):
        self.total = total
        self.counter = 0

    def update(self):
        self.counter += 1
        sys.stdout.write("Progress: %s%% %s" % (100 * self.counter / self.total, "\r"))
        sys.stdout.flush()
