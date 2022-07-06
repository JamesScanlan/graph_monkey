from data_set_iterator import DataSetIterator
import uuid

class DataSet(object):
    def __init__(self, name):
        self.data_items = []
        self.name = name
        self.id = self.__generate_id()

    def __generate_id(self):
        return uuid.uuid4()

    def add_data_items(self, data_items):
        self.data_items = data_items

    def add_data_item(self, data_item):
        self.data_items.append(data_item)

    def __len__(self):
        return len(self.data_items)

    def __iter__(self):
        return DataSetIterator(self)

    def __getitem__(self, index):
        if index > (len(self.data_items) - 1):
            raise ValueError("Index presented greater than number of parsed objects")
        return self.data_items[index]

    def get_keys(self):
        keys = []
        for data_item in self:
            keys.append(data_item.key)
        return keys

    def get_values(self):
        values = []
        for data_item in self:
            values.append(data_item.value)
        return values

    def get_lowest_key(self):
        keys = self.get_keys()
        keys.sort()
        return keys[0]

    def get_highest_key(self):
        keys = self.get_keys()
        keys.sort(reverse = True)
        return keys[0]

    def clean_values(self, values):
        new_values = []
        for value in values:
            if value != None:
                new_values.append(value)
        return new_values

    def get_lowest_value(self):
        values = self.clean_values(self.get_values())
        values.sort()
        return values[0]

    def get_highest_value(self):
        values = self.clean_values(self.get_values())
        values.sort(reverse = True)
        return values[0]