from axis_config import AxisPadding


class AxisLabelsCreator(object):

    def __init__(self, low, high, format, padding = AxisPadding.DATA):
        self.axis_labels = None
        self.high = high
        self.low = low
        self.padding = padding
        self.format = format
        self.axis_labels_summarising_metric = 1
        self.axis_markers = None

 
