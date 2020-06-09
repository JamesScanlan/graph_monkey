from axis_markers_iterator import AxisMarkersIterator

class AxisMarkers(object):
    def __init__(self):
        self.markers = []

    def __len__(self):
        return len(self.markers)

    def __iter__(self):
        return AxisMarkersIterator(self)

    def __getitem__(self, index):
        if index > (len(self.markers) - 1):
            raise ValueError("Index presented greater than number of parsed objects")
        return self.markers[index]

    def __setitem__(self, index, value):
        if index > len(self.markers)-1:
            raise ValueError("Index presented greater than number of parsed objects")
        self.markers[index] = value
    
    def __delitem__(self, index):
        if index > len(self.markers)-1:
            raise ValueError("Index presented greater than number of parsed objects")
        del self.markers[index]

    def add_axis_marker(self, axis_marker):
        self.markers.append(axis_marker)