import datetime

class DataItem(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, value):
        return self.value == value

    def __gt__(self, value):
        return self.value > value

    def __lt__(self, value):
        return self.value < value

    def __get_data_type(self, item):
        if isinstance(item, int):
            return int
        elif isinstance(item, datetime.date):
            return datetime.date
        elif isinstance(item, str):
            return str
        else:
            return None

    def get_key_data_type(self):
        return self.__get_data_type(self.key)

    def get_value_data_type(self):
        return self.__get_data_type(self.value)

    
    
