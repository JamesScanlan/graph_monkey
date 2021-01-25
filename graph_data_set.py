from data_set import DataSet
from data_set_iterator import DataSetIterator
from axis_type_enum import AxisType

class GraphDataSet(object):
    def __init__(self, data_set, axis_type):
        self.data_set = data_set
        self.axis_type = axis_type
        self.name = data_set.name
        self.id = self.data_set.id

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __eq__(self, other):
        return self.name == other.name

    def __len__(self):
        return len(self.data_set)

    def __iter__(self):
        return DataSetIterator(self.data_set)

    def __getitem__(self, index):
        return self.data_set[index]

    def get_keys(self):
        return self.data_set.get_keys()

    def get_values(self):
        return self.data_set.get_values()

    def get_lowest_key(self):
        return self.data_set.get_lowest_key()

    def get_highest_key(self):
        return self.data_set.get_highest_key()

    def get_lowest_value(self):
        return self.data_set.get_lowest_value()
        
    def get_highest_value(self):
        return self.data_set.get_highest_value()
