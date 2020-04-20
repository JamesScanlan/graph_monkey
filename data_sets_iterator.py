class DataSetsIterator(object):
    def __init__(self, data_sets):
        self._data_sets = data_sets
        self._index = -1

    def __next__(self):
        if self._index < (len(self._data_sets) - 1):
            self._index += 1
            return self._data_sets[self._index]
        raise StopIteration