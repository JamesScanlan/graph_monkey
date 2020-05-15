from axis_meta_data_iterator import AxisMetaDataIterator

class AxisMetaData(object):
    def __init__(self):
        self.items = []

    def get_axis_meta_data_item(self, data_set_name):
        for meta_data_item in self.items:
            if meta_data_item.data_set_name == data_set_name:
                return meta_data_item
        return None

    def add_axis_meta_data_item(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return AxisMetaDataIterator(self)

    def __getitem__(self, index):
        if index > (len(self.values) - 1):
            raise ValueError("Index presented greater than number of parsed objects")
        return self.values[index]