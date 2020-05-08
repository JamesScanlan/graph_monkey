class AxisConfig(object):
    def __init__(self, title, datatype, data_format = ''):
        self.title = title
        self.datatype = datatype
        self.format = data_format
        self.axis_config_items = []

    def add_axis_config_item(self, axis_config_item):
        self.axis_config_items.append(axis_config_item)

    def __str__(self):
        output = ''
        counter = 0
        for axis_config_item in self.axis_config_items:
            output += str(axis_config_item)
            counter += 1
            if counter < (len(self.axis_config_items) ):
                output += ', '

        return str(str(self.title) + ',' + self.__handle_none(self.datatype)) + ', ' +  str(self.__handle_none(self.format) + ' Config Items: ' + output)

    def __handle_none(self, value):
        if value == None:
            return ''
        else:
            return value