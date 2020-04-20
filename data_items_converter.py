from data_set import DataSet
from data_item import DataItem

def create_data_set(key_items, value_items, name = ""):
    data_items = []
    for key_counter in range(0, len(key_items)):
        key = key_items[key_counter]
        if key_counter < len(value_items):
            value = value_items[key_counter]
        else:
            value = None
        data_items.append(DataItem(key, value))

    ds = DataSet(name)
    ds.add_data_items(data_items)
    return ds