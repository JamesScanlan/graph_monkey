from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator

class IntAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high):
        super().__init__(low, high)
        self.__set_axis_labels()

    def __zero_pad(self, instances):
        padding = ''
        for instances in range(0, instances):
            padding += '0'
        return padding

    def __determine_interval(self, low_value, value_range):
        if value_range <= 25:
            return 1
        else:
            return int("1" + self.__zero_pad(len(str(value_range)) -1))
        
    def __set_axis_labels(self):
        value_range = self.high - self.low
        interval = self.__determine_interval(self.low, value_range)
        axis_labels = []
        for counter in range(self.low, self.high + interval, interval):
            axis_labels.append(AxisLabel(counter, str(counter)))
        
        self.axis_labels = axis_labels