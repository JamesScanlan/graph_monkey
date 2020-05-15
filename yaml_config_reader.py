import yaml
import io
from axis_config import AxisConfig
from axis_config_item import AxisConfigItem
from axis_config_item import AxisType
import datetime
from time_value import TimeValue

class YAMLConfigReader(object):
    def __init__(self):
        self.title = ""
        self.file_names = {}
        self.file_format = ''
        self.x_axis_config = None
        self.y_axis_config = None
        self.single_y_axis = True

    def __str__(self):
        return str(self.file_names) + ', ' + str(self.file_format) + ', ' + str(self.x_axis_config) + ', ' + str(self.y_axis_config)

    def read_file(self, file_name):
        file = open(file_name, 'r')
        documents = yaml.safe_load_all(file)
        for document in documents:
            if document is not None:
                self.title = document['title']
                file_names = {}
                for file_name in document['data']['files']:
                    file_names[file_name['file']] = file_name['name']
                self.file_names = file_names
                self.file_format = str(document['data']['format'])
                
                self.x_axis_config = AxisConfig(self.__navigate_path(document,'x','title'))
                self.__read_axis_config_item(self.x_axis_config, document['x']['indexes'])
                
                self.__handle_y_axes(document)                
                self.y_axis_config = AxisConfig(self.__navigate_path(document,'y','title'))
                self.__read_axis_config_item(self.y_axis_config, document['y']['indexes'])    
                

    def __handle_y_axes(self, document):
        axes_value = self.__parse_dictionary_item(document["y"], "axes")
        if axes_value != None:
            if axes_value == 'Multiple':
                self.single_y_axis = False

    def __read_axis_config_item(self, axis_config, data):
        for data_item in data:         
            axis_config.add_axis_config_item(AxisConfigItem(int(data_item['index']), data_item['name'], self.__set_type(data_item['datatype']), self.__set_axis_type(self.__parse_dictionary_item(data_item,'axis')), self.__parse_dictionary_item(data_item,'format')))

    def __parse_dictionary_item(self, reference_dictionary, key_name):
        if key_name in reference_dictionary:
            return reference_dictionary[key_name]
        else:
            return None 


    def __set_axis_type(self, axis_type):
        if axis_type is None:
            return AxisType.PRIMARY

        if str(axis_type).upper() == "SECONDARY":
            return AxisType.SECONDARY
        else:
            return AxisType.PRIMARY

    def __set_type(self, type_name):
        if type_name == 'datetime':
            return datetime.datetime
        if type_name == 'int':
            return int
        if type_name == 'float':
            return float
        if type_name == 'date':
            return datetime.date
        if type_name == 'time':
            return TimeValue
        if type_name == 'string':
            return str
        return None

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