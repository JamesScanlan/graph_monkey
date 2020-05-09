from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator
from float_parser import FloatParser

class FloatAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high):
        super().__init__(low, high)
        self.__set_axis_labels()

    def __zero_pad(self, instances):
        padding = ''
        for instances in range(0, instances):
            padding += '0'
        return padding

    def __determine_interval(self, low_value, value_range):
        parsed_value = FloatParser(low_value)
        
        zero_padding = ''
        for padding_counter in range(0, len(str(parsed_value.frac_part)) -1):
            zero_padding += '0'
        return float('0.' + zero_padding + '1')
        # if value_range <= 25:
        #     return 1
        # else:
        #     return float('1' + self.__zero_pad(len(str(value_range)) -1))
        
    def __set_axis_labels(self):
        value_range = self.high - self.low
        interval = self.__determine_interval(self.low, value_range)
        interval_scale = len(str(FloatParser(interval).frac_part))
        axis_labels = []
        format_string = "{:." + str(interval_scale) + "f}"
        exit_loop = False
        value = self.low
        while exit_loop == False:
            axis_labels.append(AxisLabel(value, str(value)))
            value += interval
            value = float(format_string.format(value))
            if value > (self.high + interval):
                exit_loop = True
        self.axis_labels = axis_labels