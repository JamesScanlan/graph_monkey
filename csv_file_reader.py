import csv
import datetime
from time_value import TimeValue
from csv_values import CSVValues

class CSVFileReader(object):

    def __init__(self):
        self.__x_values = []  
        self.__y_values = []

    def get_x_values(self):
        return self.__x_values

    def get_y_values(self):
        return self.__y_values

    def read_file(self, file_name, x_axis_config, y_axis_config):
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            first_row = True

            y_values = {}
            for y_axis_config_item in y_axis_config.axis_config_items:
                y_values[y_axis_config_item.name] = CSVValues(y_axis_config_item.name)

            for row in reader:
                if first_row == True:
                    first_row = False
                else:
                    self.__x_values.append(self.__parse_value(row[x_axis_config.axis_config_items[0].index], x_axis_config.datatype, x_axis_config.format))
                    for y_axis_config_item in y_axis_config.axis_config_items:
                        y_values[y_axis_config_item.name].add(self.__parse_value(row[y_axis_config_item.index], y_axis_config.datatype, y_axis_config.format))

            for y_values_set in y_values:
                self.__y_values.append(y_values[y_values_set])
                    

    def __parse_value(self, value, datatype, format = None):
        if datatype is int:
            return self.__parse_int(value)
        if datatype is datetime.datetime:
            return self.__parse_datetime(value, format)
        if datatype is datetime.date:
            return self.__parse_date(value, format)
        if datatype is str:
            return self.__parse_str(value)
        if datatype is TimeValue:
            return self.__parse_time_value(value, format)
        return None

    def __parse_time_value(self, value, parse_format):
        d = datetime.datetime.strptime(value, parse_format) 
        return TimeValue(d.hour, d.minute)

    def __parse_datetime(self, value, parse_format):
        return datetime.datetime.strptime(value, parse_format)

    def __parse_date(self, value, parse_format):
        d = datetime.datetime.strptime(value, parse_format) 
        return datetime.date(d.year, d.month, d.day)

    def __parse_int(self, value):
        return int(value)

    def __parse_str(self, value):
        return str(value)

