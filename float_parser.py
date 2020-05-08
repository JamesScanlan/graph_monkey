class FloatParser(object):
    def __init__(self, value):
        self.original_value = value
        self.whole_part = 0
        self.frac_part = 0
        self.__parse_value()

    def __parse_value(self):
        string_version = str(self.original_value)
        pos = string_version.find('.')
        if pos > -1:
            self.whole_part = int(string_version[0:pos])
            self.frac_part = int(string_version[pos+1: len(string_version)])
        else:
            self.whole_part = int(self.original_value)
            
    def __str__(self):
        return str(self.original_value)