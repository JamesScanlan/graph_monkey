class AxisConfigItem(object):
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def __str__(self):
        return str(self.index) + ', ' + self.name