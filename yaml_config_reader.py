import yaml
import io
from axis_config import AxisConfig
from axis_config_item import AxisConfigItem
import datetime
from time_value import TimeValue

#{'file': {'name': '034_errors.csv', 'format': 'text/csv'}, 'x': {'index': 0, 'datatype': 'datetime.datetime', 'format': '%d/%m/%Y %H:%M'}, 'y': {'index': 1, 'datatype': 'int'}}

class YAMLConfigReader(object):
    def __init__(self):
       self.file_name = ''
       self.file_format = ''
       self.x_axis_config = None
       self.y_axis_config = None

    def __str__(self):
        return str(self.file_name) + ', ' + str(self.file_format) + ', ' + str(self.x_axis_config) + ', ' + str(self.y_axis_config)


    def read_file(self, file_name):
        file = open(file_name, 'r')
        documents = yaml.safe_load_all(file)
        for document in documents:
            if document is not None:
                self.file_name = str(document['file']['name'])
                self.file_format = str(document['file']['format'])
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

        
        # for arg in args:
        #     for key, value in document.items():
        #         if key == arg:
        #             if args.index(key) < len(args):
        #                 return self.__validate_path(document,self.__set_args(args.index(key), args))
        #             else:
        #                 return value
        # return None

    def __set_args(self, index, *args):
        s = slice(index, len(args))
        return args[s]

    # def print_all_leaf_nodes(self, data):
    #     if isinstance(data, dict):
    #         print('dict')
    #         for item in data.values():
    #             self.print_all_leaf_nodes(item)
    #     elif isinstance(data, list) or isinstance(data, tuple):
    #         print('list or tuple')
    #         for item in data:
    #             self.print_all_leaf_nodes(item)
    #     else:
    #         print('something else')
    #         print(data)

    # def __validate_path(self, data, *args):
    #     for arg in args:
    #         print(self.__search_data(data,arg))

    # def __search_data(self, data, arg):
    #     if isinstance(data, dict):
    #         for item in data.keys():
    #             #this is fucked up.  need my proper head on to recursively loop
    #             return self.__search_data(data[item], arg)
    #     elif isinstance(data, list) or isinstance(data, tuple):
    #         for item in data:
    #             return self.__search_data(data[item], arg)
    #     else:
    #         print(data, arg)
    #         if data == arg:
    #             return data
    #     return None