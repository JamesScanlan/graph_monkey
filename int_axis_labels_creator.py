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
            axis_labels.append(AxisLabel(counter, self.__formatLabel(counter)))
        
        self.axis_labels = axis_labels

    def __formatLabel(self, value):
        string_value = str(value)
        formatted_output = ''
        if len(string_value) > 3:
            for counter in range(len(string_value), 0, -3):
                formatted_output = ',' + string_value[counter - 3 : counter] + formatted_output
                if (counter - 3) <= 3:
                    formatted_output = string_value[0:counter - 3] + formatted_output
                    break
        else:
            formatted_output = string_value
        return formatted_output

if __name__ == "__main__":
    axis_labels = IntAxisLabelsCreator(0,100000).axis_labels
    for axis_label in axis_labels:
        print(str(axis_label))

