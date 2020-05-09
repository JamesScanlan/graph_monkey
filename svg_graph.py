import svg_monkey
from svg_point import Point
import bubblesort
import datetime
from date_axis_labels_creator import DateAxisLabelsCreator
from datetime_axis_labels_creator import DateTimeAxisLabelsCreator
from time_value_axis_labels_creator import TimeValueAxisLabelsCreator
from int_axis_labels_creator import IntAxisLabelsCreator
from float_axis_labels_creator import FloatAxisLabelsCreator
from time_value import TimeValue
from axis import Axis
from data_sets import DataSets
from colours_palete import ColoursPalete
from float_parser import FloatParser

class Graph(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.bottom_margin = 100
        self.left_margin = 200
        self.svg_contents = ''
        self.x_axis = None
        self.y_axis = None
        self.data_sets = DataSets()

        self.x_axis_title = ''
        self.y_axis_title = ''
        self.title = ''


    def __draw_graph_title(self):
        if self.title != '':
            point = Point(self.left_margin + (self.width / 2), self.bottom_margin - (self.bottom_margin / 3))
            self.svg_contents += svg_monkey.write_text(point, self.title, 0, 'title')

    def __draw_x_axis_title(self, rotated_labels = False):
        if self.x_axis.title != '':
            y_buffer = 60
            if rotated_labels == True:
                y_buffer += 95
            point = Point(self.left_margin + (self.width/2), self.bottom_margin + self.height + y_buffer)
            self.svg_contents += svg_monkey.write_text(point, self.x_axis.title, 0, 'axis_title')

    def __draw_y_axis_title(self, offset = 75):
        if self.y_axis.title != '':
            point = Point(self.left_margin - offset, self.bottom_margin + (self.height/2))
            self.svg_contents += svg_monkey.write_text(point, self.y_axis.title, 270, 'axis_title')

    def __draw_x_axis(self):
        if self.x_axis.data_type is int:
            self.__draw_x_axis_for_int()
        if self.x_axis.data_type is datetime.date:
            self.__draw_x_axis_for_date()
        if self.x_axis.data_type is datetime.datetime:
            self.__draw_x_axis_for_datetime()
        if self.x_axis.data_type is TimeValue:
            self.__draw_x_axis_for_time_value()

    def __draw_x_axis_for_int(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin + self.width, self.bottom_margin + self.height)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.x_axis.markers != None:
            for counter in range(0, len(self.x_axis.markers)):
                start_point = Point(self.left_margin + (((self.x_axis.markers[counter].value - self.x_axis.low) / (self.x_axis.high - self.x_axis.low)) * self.width), self.bottom_margin + self.height)
                end_point = Point(self.left_margin + (((self.x_axis.markers[counter].value -self.x_axis.low) / (self.x_axis.high - self.x_axis.low)) * self.width), self.bottom_margin + self.height + 15)
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                start_point = Point(self.left_margin -5 + (((self.x_axis.markers[counter].value - self.x_axis.low) / (self.x_axis.high - self.x_axis.low)) * self.width), self.bottom_margin + self.height + 30)
                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].label),0,'axis_label')
        self.__draw_x_axis_title()
        
    def __draw_x_axis_for_date(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin + self.width, self.bottom_margin + self.height)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.x_axis.markers != None:
            for counter in range(0, len(self.x_axis.markers)):
                start_point = Point(self.left_margin + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height)
                end_point = Point(self.left_margin + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height + 15)
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                start_point = Point(self.left_margin -5 + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height + 30)
                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].label),0,'axis_label')
        self.__draw_x_axis_title()

    def __draw_x_axis_for_datetime(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin + self.width, self.bottom_margin + self.height)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        rotated_labels = False
        if self.x_axis.markers != None:
            for counter in range(0, len(self.x_axis.markers)):
                start_point = Point(self.left_margin + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height)
                end_point = Point(self.left_margin + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height + 15)
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                
                rotation = 0
                y_position = self.bottom_margin + self.height + 30
                if str(self.x_axis.markers[counter].label).find(' ') > -1:
                    if rotated_labels == False:
                        rotated_labels = True
                    rotation = 90
                    y_position = y_position + 45
                
                start_point = Point(self.left_margin -5 + ((counter/ (len(self.x_axis.markers)-1)) * self.width), y_position)
                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].label),rotation,'axis_label')
        self.__draw_x_axis_title(rotated_labels)

    def __draw_x_axis_for_time_value(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin + self.width, self.bottom_margin + self.height)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.x_axis.markers != None:
            for counter in range(0, len(self.x_axis.markers)):
                start_point = Point(self.left_margin + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height)
                end_point = Point(self.left_margin + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height + 15)
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                start_point = Point(self.left_margin -5 + ((counter/ (len(self.x_axis.markers)-1)) * self.width), self.bottom_margin + self.height + 30)
                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].label),0,'axis_label')
        self.__draw_x_axis_title()



    def __draw_y_axis(self):
        if self.y_axis.data_type is int:
            self.__draw_y_axis_for_int()
        if self.y_axis.data_type is float:
            self.__draw_y_axis_for_float()
        if self.y_axis.data_type is datetime.date:
            self.__draw_y_axis_for_date()
        if self.y_axis.data_type is datetime.datetime:
            self.__draw_y_axis_for_datetime()
        if self.y_axis.data_type is TimeValue:
            self.__draw_y_axis_for_time_value()
    
    def __draw_y_axis_for_int(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin, self.bottom_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.y_axis.markers != None:
            for counter in range(0, len(self.y_axis.markers)): #, 100
                start_point = Point(self.left_margin, (self.bottom_margin + self.height) - (((self.y_axis.markers[counter].value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height))
                end_point = Point(self.left_margin -15, (self.bottom_margin + self.height) - (((self.y_axis.markers[counter].value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                label_point = Point(self.left_margin - 35, (self.bottom_margin + self.height) - (((self.y_axis.markers[counter].value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str((self.y_axis.markers[counter].label)),0,'axis_label')
        self.__draw_y_axis_title()

    def __draw_y_axis_for_date(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin, self.bottom_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.y_axis.markers != None:
            for counter in range(0, len(self.y_axis.markers)):
                start_point = Point(self.left_margin, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                end_point = Point(self.left_margin - 15, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                label_point = Point(self.left_margin - 75, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(self.y_axis.markers[counter].label),0,'axis_label')
        self.__draw_y_axis_title(150)

    def __draw_y_axis_for_datetime(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin, self.bottom_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.y_axis.markers != None:
            for counter in range(0, len(self.y_axis.markers)):
                start_point = Point(self.left_margin, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                end_point = Point(self.left_margin - 15, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                label_point = Point(self.left_margin - 75, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(self.y_axis.markers[counter].label),0,'axis_label')
        self.__draw_y_axis_title(150)

    def __draw_y_axis_for_time_value(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin, self.bottom_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.y_axis.markers != None:
            for counter in range(0, len(self.y_axis.markers)):
                start_point = Point(self.left_margin, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                end_point = Point(self.left_margin - 15, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                label_point = Point(self.left_margin - 75, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(self.y_axis.markers[counter].label),0,'axis_label')
        self.__draw_y_axis_title(150)

    def __draw_y_axis_for_float(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin, self.bottom_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.y_axis.markers != None:
            for counter in range(0, len(self.y_axis.markers)):
                start_point = Point(self.left_margin, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                end_point = Point(self.left_margin - 15, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                label_point = Point(self.left_margin - 75, (self.bottom_margin + self.height) - ((counter / (len(self.y_axis.markers) - 1)) * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(self.y_axis.markers[counter].label),0,'axis_label')
        self.__draw_y_axis_title(150)

    def __translate_data_to_points(self, data_set):
        points = []
        # loop_counter = 0
        for data_item in data_set:
            x = self.left_margin + round((((data_item.key - self.x_axis.low) / (self.x_axis.high - self.x_axis.low)) * self.width),2)
            y = self.bottom_margin + round(self.height - ((((data_item.value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height)), 2)
            point = Point(x, y)
            points.append(point)

        return points

    def __get_lowest_and_highest(self, values):
        sorted_values = bubblesort.bubble_sort(values)
        lowest_value = sorted_values[0]
        highest_value = sorted_values[len(values) -1]
        return lowest_value, highest_value

    def __get_value_type(self, value):
        t = type(value)
        if t is int:
            return int
        elif t is float:
            return float
        elif t is datetime.datetime:
            return datetime.datetime
        elif t is datetime.date:
            return datetime.date
        elif t is TimeValue:
            return TimeValue
        else:
            return None

    def __round_int_down(self, value, raw_range):
        revised_value = value
        if int(str(revised_value)[len(str(revised_value))-1]) != 0:
            revised_value = int(str(revised_value)[0:len(str(revised_value))-1] + '0')
        return revised_value
    
    def __round_float_down(self, value, raw_range):
        parsed_value = FloatParser(value)
        revised_value = float(str(parsed_value.whole_part) + '.' + str(parsed_value.frac_part)[0:len(str(parsed_value.frac_part))-1] + '0')
        return revised_value

    def __round_date_down(self, value, raw_range):
        if raw_range.days > 365:
            #years
            return datetime.date(value.year, 1, 1)
        elif raw_range.days > 31:
            #months
            return datetime.date(value.year, value.month, 1)
        else:
            #days
            return value #+ datetime.timedelta(-1)

    def __round_down(self, value_type, lowest_value, raw_range):
        if value_type is int:
            return self.__round_int_down(lowest_value, raw_range)
        if value_type is float:
            return self.__round_float_down(lowest_value, raw_range)
        if value_type is datetime.date or value_type is datetime.datetime or value_type is TimeValue:
            return self.__round_date_down(lowest_value, raw_range)
        return None
        

    def __evaluate_axis_data_by_type(self, lowest_value, highest_value):
        t = self.__get_value_type(lowest_value)
        raw_range = highest_value - lowest_value
        lowest_value = self.__round_down(t, lowest_value, raw_range)
        return t, lowest_value, highest_value

    def __print_out_values(self):
        for counter in range(0, len(self.x_values)):
            print(self.x_values[counter], self.y_values[counter])

    def __zero_base_for_int(self):
        if self.x_axis.data_type is int:
            if self.x_axis.low > 0:
                self.x_axis.low = 0
        if self.y_axis.data_type is int:
            if self.y_axis.low > 0:
                self.y_axis.low = 0

    def __revise_x_high_low(self):
        if self.x_axis.markers != None:
            self.x_axis.low = self.x_axis.markers[0].value
            self.x_axis.high = self.x_axis.markers[len(self.x_axis.markers) - 1].value
    
    def __revise_y_high_low(self):
        if self.y_axis.markers != None:
            self.y_axis.low = self.y_axis.markers[0].value
            self.y_axis.high = self.y_axis.markers[len(self.y_axis.markers) - 1].value

    def __evaluate_data(self, zero_base = False):
        lowest_x_value, highest_x_value = self.data_sets.get_lowest_and_highest_key()
        lowest_y_value, highest_y_value = self.data_sets.get_lowest_and_highest_value()
        
        x_data_type, x_low, x_high = self.__evaluate_axis_data_by_type(lowest_x_value, highest_x_value)
        y_data_type, y_low, y_high = self.__evaluate_axis_data_by_type(lowest_y_value, highest_y_value)
        # print(x_low, x_high)
        # print(y_low, y_high)
        self.x_axis = Axis(x_low, x_high, x_data_type)
        self.y_axis = Axis(y_low, y_high, y_data_type)

        if zero_base == True:
            self.__zero_base_for_int()

        if x_data_type is int:
            self.x_axis.markers = IntAxisLabelsCreator(self.x_axis.low, self.x_axis.high).axis_labels
        elif x_data_type is datetime.date:
            self.x_axis.markers = DateAxisLabelsCreator(self.x_axis.low, self.x_axis.high).axis_labels
        elif x_data_type is datetime.datetime:
            self.x_axis.markers = DateTimeAxisLabelsCreator(self.x_axis.low, self.x_axis.high).axis_labels
        elif x_data_type is TimeValue:
            self.x_axis.markers = TimeValueAxisLabelsCreator(self.x_axis.low, self.x_axis.high).axis_labels

        self.__revise_x_high_low()

        if y_data_type is int:
            self.y_axis.markers = IntAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels
        elif y_data_type is float:
            self.y_axis.markers = FloatAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels
        elif y_data_type is datetime.date:
            self.y_axis.markers = DateAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels
        elif y_data_type is datetime.datetime:
            self.y_axis.markers = DateTimeAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels
        elif y_data_type is TimeValue:
            self.y_axis.markers = TimeValueAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels

        self.__revise_y_high_low()

    def __write_point_markers(self, points, display_markers=True, display_labels=True, color="", label = ""):
        for point in points:
            if display_markers == True:
                self.svg_contents += svg_monkey.write_circle(point, 4, color)
        if display_labels == True:
            self.svg_contents += svg_monkey.write_text(Point(point.x + 10, point.y + 5), label, 0, 'legend_item', color)

    def __set_axes_titles(self):
        if self.x_axis != None:
            self.x_axis.title = self.x_axis_title
        if self.y_axis != None:
            self.y_axis.title = self.y_axis_title

    def __draw_legend(self):
        contents = ''
        
        colours_palete = ColoursPalete()
        spacer = 20
        left = self.left_margin + self.width + 50

        contents += svg_monkey.write_text(Point(left, self.bottom_margin), 'Legend', 0, 'legend_item_title')

        for data_set in self.data_sets:
            colour = colours_palete.get_next_colour()
            contents += svg_monkey.write_line(Point(left - 30,self.bottom_margin + spacer - 3), Point(left -10,self.bottom_margin + spacer - 3), colour)
            contents += svg_monkey.write_text(Point(left, self.bottom_margin + spacer), data_set.name, 0, 'legend_item', colour)
            spacer += 20
        return contents

    def draw_graph(self):
        self.svg_contents += svg_monkey.write_svg_start(self.left_margin + self.width + self.left_margin, self.bottom_margin + self.height + (self.bottom_margin * 2))

        self.__evaluate_data(True)    
        self.__draw_graph_title()
        self.__set_axes_titles()
        self.__draw_x_axis()
        self.__draw_y_axis()

        colours_palete = ColoursPalete()        
        for data_set in self.data_sets:
            colour = colours_palete.get_next_colour()
            points = self.__translate_data_to_points(data_set)
            self.svg_contents += svg_monkey.write_lines(points, colour)
            self.__write_point_markers(points, False, False, colour, data_set.name)

        self.svg_contents += self.__draw_legend()

        self.svg_contents += svg_monkey.write_svg_end()


