from data_sets_iterator import DataSetsIterator
from data_item import DataItem

class DataSets(object):
    def __init__(self):
        self.data_sets = []
    
    def __sizeof__(self):
        return self.len()

    def __len__(self):
        return len(self.data_sets)

    def add_data_set(self, data_set):
        if isinstance(data_set[0], DataItem) == True:
            self.data_sets.append(data_set)    

    def __iter__(self):
        return DataSetsIterator(self)

    def __getitem__(self, index):
        if index > (len(self.data_sets) - 1):
            raise ValueError("Index presented greater than number of parsed objects")
        return self.data_sets[index]

    def get_lowest_key(self):
        lowest = None
        for data_set in self.data_sets:
            lowest_in_data_set = data_set.get_lowest_key()
            if lowest == None:
                lowest = lowest_in_data_set
            else:
                if lowest_in_data_set < lowest:
                    lowest = lowest_in_data_set
        return lowest

    def get_lowest_value(self):
        lowest = None
        for data_set in self.data_sets:
            lowest_in_data_set = data_set.get_lowest_value()
            if lowest == None:
                lowest = lowest_in_data_set
            else:
                if lowest_in_data_set < lowest:
                    lowest = lowest_in_data_set
        return lowest

    def get_highest_key(self):
        highest = None
        for data_set in self.data_sets:
            highest_in_data_set = data_set.get_highest_key()
            if highest == None:
                highest = highest_in_data_set
            else:
                if highest_in_data_set > highest:
                    highest = highest_in_data_set
        return highest

    def get_highest_value(self):
        highest = None
        for data_set in self.data_sets:
            highest_in_data_set = data_set.get_highest_value()
            if highest == None:
                highest = highest_in_data_set
            else:
                if highest_in_data_set > highest:
                    highest = highest_in_data_set
        return highest

    def get_lowest_and_highest_key(self):
        return self.get_lowest_key(), self.get_highest_key()

    def get_lowest_and_highest_value(self):
        return self.get_lowest_value(), self.get_highest_value()

