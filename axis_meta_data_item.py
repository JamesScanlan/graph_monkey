from axis_type_enum import AxisType

class AxisMetaDataItem(object):
    def __init__(self, data_set_name, axis_type):
        self.data_set_name = data_set_name
        self.axis_type = axis_type

    def __str__(self):
        return str(self.data_set_name) + ', ' + str(self.axis_type)