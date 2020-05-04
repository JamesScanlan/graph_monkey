class CSVValuesIterator(object):
    def __init__(self, values):
        self._values = values
        self._index = -1

    def __next__(self):
        if self._index < (len(self._values) - 1):
            self._index += 1
            return self._values[self._index]
        raise StopIteration
