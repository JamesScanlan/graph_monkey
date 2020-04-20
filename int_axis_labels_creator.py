from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator

class IntAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high):
        super().__init__(low, high)
        self.__set_axis_labels()

    def __set_axis_labels(self):
        value_range = self.high - self.low
        interval = len(str(value_range)) -1
        if interval == 0:
            interval = 1

        axis_labels = []
        for counter in range(self.low, self.high + interval, interval):
            axis_labels.append(AxisLabel(counter, str(counter)))
        
        self.axis_labels = axis_labels