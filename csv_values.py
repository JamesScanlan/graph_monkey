from csv_values_iterator import CSVValuesIterator 

class CSVValues(object):
    def __init__(self, name):
        self.values = []
        self.name = name

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return CSVValuesIterator(self)

    def __getitem__(self, index):
        if index > (len(self.values) - 1):
            raise ValueError("Index presented greater than number of parsed objects")
        return self.values[index]

    def add(self, value):
        self.values.append(value)

    