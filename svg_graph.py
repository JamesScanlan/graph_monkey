import svg_monkey
from svg_point import Point
import bubblesort
import datetime
from date_axis_labels_creator import DateAxisLabelsCreator
from int_axis_labels_creator import IntAxisLabelsCreator
from axis import Axis
from data_sets import DataSets
from colours_palete import ColoursPalete

class Graph(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.bottom_margin = 200
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

    def __draw_x_axis_title(self):
        if self.x_axis.title != '':
            point = Point(self.left_margin + (self.width/2), self.bottom_margin + self.height + 75)
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
                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].label))
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
                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].label))
        self.__draw_x_axis_title()

    def __draw_y_axis(self):
        if self.y_axis.data_type is int:
            self.__draw_y_axis_for_int()
        if self.y_axis.data_type is datetime.date:
            self.__draw_y_axis_for_date()
    
    def __draw_y_axis_for_int(self):
        start_point = Point(self.left_margin, self.bottom_margin + self.height)
        end_point = Point(self.left_margin, self.bottom_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point)

        if self.y_axis.markers != None:
            for counter in range(0, len(self.y_axis.markers)):
                start_point = Point(self.left_margin, (self.bottom_margin + self.height) - (((self.y_axis.markers[counter].value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height))
                end_point = Point(self.left_margin -15, (self.bottom_margin + self.height) - (((self.y_axis.markers[counter].value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point)

                label_point = Point(self.left_margin - 35, (self.bottom_margin + self.height) - (((self.y_axis.markers[counter].value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str((self.y_axis.markers[counter].label)))
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
                self.svg_contents += svg_monkey.write_text(label_point, str(self.y_axis.markers[counter].label))
        self.__draw_y_axis_title(150)

    def __translate_data_to_points(self, data_set):
        points = []
        for data_item in data_set:
            x = self.left_margin + (((data_item.key - self.x_axis.low) / (self.x_axis.high - self.x_axis.low)) * self.width)
            y = self.bottom_margin + self.height - ((((data_item.value - self.y_axis.low) / (self.y_axis.high - self.y_axis.low)) * self.height))
            point = Point(x, y)
            points.append(point)
        return points

    def __get_lowest_and_highest(self, values):
        sorted_values = bubblesort.bubble_sort(values)
        lowest_value = sorted_values[0]
        highest_value = sorted_values[len(values) -1]
        return lowest_value, highest_value

    def __get_value_type(self, value):
        if isinstance(value, int) == True:
            return int
        elif isinstance(value, datetime.date) == True:
            return datetime.date
        else:
            return None

    #this logic needs improving
    def __round_int_down(self, value, raw_range):
        value_digit_count = len(str(value))
        raw_range_digit_count = len(str(value))
        interval = 0
        if value_digit_count == raw_range_digit_count:
            interval = value_digit_count
        else:
            interval = value_digit_count

        revised_value = value
        
        if (interval == 1 and value == 0) == False:
            exit_loop = False
            
            while exit_loop == False:
                revised_value -= interval
                if revised_value == 0:
                    exit_loop = True
                elif revised_value % interval == 0:
                    exit_loop = True
          
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

    def __set_axis_for_int(self, lowest_value, highest_value):
        #need to round down and up lowest and highest
        raw_range = highest_value - lowest_value
        lowest_value = self.__round_int_down(lowest_value, raw_range)
        return int, lowest_value, highest_value

    def __set_axis_for_date(self, lowest_value, highest_value):
        raw_range = highest_value - lowest_value
        lowest_value = self.__round_date_down(lowest_value, raw_range)
        return datetime.date, lowest_value, highest_value

    def __evaluate_axis_data_by_type(self, lowest_value, highest_value):
        t = self.__get_value_type(lowest_value)
        if t is int:
            return self.__set_axis_for_int(lowest_value, highest_value)
        if t is datetime.date:
            return self.__set_axis_for_date(lowest_value, highest_value)
        return None

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

        self.x_axis = Axis(x_low, x_high, x_data_type)
        self.y_axis = Axis(y_low, y_high, y_data_type)

        if zero_base == True:
            self.__zero_base_for_int()

        if x_data_type is int:
            self.x_axis.markers = IntAxisLabelsCreator(self.x_axis.low, self.x_axis.high).axis_labels
        elif x_data_type is datetime.date:
            self.x_axis.markers = DateAxisLabelsCreator(self.x_axis.low, self.x_axis.high).axis_labels

        self.__revise_x_high_low()

        if y_data_type is int:
            self.y_axis.markers = IntAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels
        elif y_data_type is datetime.date:
            self.y_axis.markers = DateAxisLabelsCreator(self.y_axis.low, self.y_axis.high).axis_labels

        self.__revise_y_high_low()

    def __write_point_markers(self, points, color="", label = ""):
        for point in points:
            self.svg_contents += svg_monkey.write_circle(point, 4, color)
        self.svg_contents += svg_monkey.write_text(Point(point.x + 10, point.y + 5), label, 0, 'legend_item', color)

    def __set_axes_titles(self):
        if self.x_axis != None:
            self.x_axis.title = self.x_axis_title
        if self.y_axis != None:
            self.y_axis.title = self.y_axis_title

    def __draw_legend(self):
        contents = ""
        point = Point(20, 20)
        contents += svg_monkey.write_text(point, 'Legend', 0, 'legend_item')
        
        spacer = 20
        for data_set in self.data_sets:
            point = Point(20, 20 + spacer)
            contents += svg_monkey.write_text(point, data_set.name)
            spacer += 20
        return contents

    def draw_graph(self):
        self.svg_contents += svg_monkey.write_svg_start(self.left_margin + self.width + self.left_margin, self.bottom_margin + self.height + self.bottom_margin)

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
            self.__write_point_markers(points, colour, data_set.name)

        self.svg_contents += svg_monkey.write_svg_end()

    def draw_legend(self):
        legend = svg_monkey.write_svg_start(300, 500)
        legend += self.__draw_legend()
        legend += svg_monkey.write_svg_end()
        return legend

