from axis_type_enum import AxisType

class AxisConfigItem(object):
    def __init__(self, index, name, data_type, axis_type, input_format, output_format=None):
        self.index = index
        self.name = name
        self.data_type = data_type
        self.axis_type = axis_type
        self.input_format = input_format
        self.output_format = output_format
        
    def __str__(self):
        return str(self.index) + ', ' + self.name + ', ' + str(self.axis_type) + ', ' + str(self.format)