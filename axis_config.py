class AxisConfig(object):
    def __init__(self, title):
        self.title = title
        self.axis_config_items = []

    def add_axis_config_item(self, axis_config_item):
        self.axis_config_items.append(axis_config_item)

    def get_axis_config_item(self, name):
        for axis_config_item in self.axis_config_items:
            if axis_config_item.name == name:
                return axis_config_item
        return None

    def __str__(self):
        output = ''
        counter = 0
        for axis_config_item in self.axis_config_items:
            output += str(axis_config_item)
            counter += 1
            if counter < (len(self.axis_config_items) ):
                output += ', '

        return str(str(self.title) + ', Config Items: ' + output)

    def __handle_none(self, value):
        if value == None:
            return ''
        else:
            return value