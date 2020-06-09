from axis_type_enum import AxisType

class Axis(object):
    def __init__(self, low, high, data_type, title = ''):
        self.low = low
        self.high = high
        self.title = ''
        self.markers = None
        self.data_type = data_type
        self.axis_type = AxisType.PRIMARY

    def set_axis_type(self, axis_type):
        self.axis_type = axis_type
