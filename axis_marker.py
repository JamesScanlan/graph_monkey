class AxisMarker(object):
    def __init__(self, marker, percentile):
        self.marker = marker
        self.percentile = percentile

    def __eq__(self, value):
        return self.value == value

    def __gt__(self, value):
        return self.value > value

    def __lt__(self, value):
        return self.value < value

    def __str__(self):
        return str(self.marker) + str(' ') + str(self.percentile)