import yaml
import io
from axis_config import AxisConfig
from axis_config_item import AxisConfigItem
import datetime
from time_value import TimeValue

class YAMLConfigReader(object):
    def __init__(self):
       self.file_names = []
       self.file_format = ''
       self.x_axis_config = None
       self.y_axis_config = None

    def __str__(self):
        return str(self.file_names) + ', ' + str(self.file_format) + ', ' + str(self.x_axis_config) + ', ' + str(self.y_axis_config)

    def read_file(self, file_name):
        file = open(file_name, 'r')
        documents = yaml.safe_load_all(file)
        for document in documents:
            if document is not None:
                for file_name in document['files']['names']:
                    self.file_names.append(file_name['name'])
                self.file_format = str(document['files']['format'])
                self.x_axis_config = AxisConfig(self.__set_type(self.__navigate_path(document,'x','datatype')), self.__navigate_path(document,'x','format'))
                self.__read_axis_config_item(self.x_axis_config, document['x']['indexes'])
                self.y_axis_config = AxisConfig(self.__set_type(self.__navigate_path(document,'y','datatype')), self.__navigate_path(document,'y','format'))
                self.__read_axis_config_item(self.y_axis_config, document['y']['indexes'])
                

    def __read_axis_config_item(self, axis_config, data):
        for data_item in data:
            axis_config.add_axis_config_item(AxisConfigItem(int(data_item['index']), data_item['name']))

    def __set_type(self, type_name):
        if type_name == 'datetime':
            return datetime.datetime
        if type_name == 'int':
            return int
        if type_name == 'date':
            return datetime.date
        if type_name == 'time':
            return TimeValue
        return str

    def __navigate_path(self, data, *args):
        found_value = None
        for arg in args:
            if isinstance(data, dict):
                found_value = self.__search_dict_by_key(data, arg)
            if found_value is not None:
                data = found_value 
        return found_value    

    def __search_dict_by_key(self, data, key_to_find):
        for key, value in data.items():
            if key == key_to_find:
                return value
        return None    

    def __set_args(self, index, *args):
        s = slice(index, len(args))
        return args[s]