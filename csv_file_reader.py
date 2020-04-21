import csv
import datetime
from time_value import TimeValue

class CSVFileReader(object):

    def __init__(self):
        self.__x_values = []
        self.__y_values = []
        
    def get_x_values(self):
        return self.__x_values

    def get_y_values(self):
        return self.__y_values

    def read_file(self, file_name):
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            first_row = True
            for row in reader:
                if first_row == True:
                    first_row = False
                else:
                    d = datetime.datetime.strptime(row[0],'%d/%m/%Y %H:%M')
                    self.__x_values.append(TimeValue(d.hour, d.minute))
                    self.__y_values.append(int(row[1]))
