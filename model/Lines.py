class Lines(object):
    def __init__(self):
        self.lines = []

    def add(self, line):
        self.lines.append(line)

    def get(self):
        return self.lines
