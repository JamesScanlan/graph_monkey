class GraphDataSetsIterator(object):
    def __init__(self, data_set):
        self._data_set = data_set
        self._index = -1

    def __next__(self):
        if self._index < (len(self._data_set) - 1):
            self._index += 1
            return self._data_set[self._index]
        raise StopIteration
