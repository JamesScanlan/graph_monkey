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
from graph_data_sets import GraphDataSets
from hsl_colours_palete import HSLColoursPalete
from float_parser import FloatParser
from axis_type_enum import AxisType
import copy

class Graph(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.top_margin = 0
        self.bottom_margin = 0
        self.left_margin = 0
        self.right_margin = 0
        self.svg_contents = ''
        self.svg_legend_title_contents = ''
        self.svg_legend_contents = ''
        self.x_axis = None
        self.x_axis_format = None # why only one format
        self.y_primary_axis = None
        self.y_secondary_axis = None
        self.data_sets = GraphDataSets()
        self.additional_axis_meta_data = None
        self.x_axis_title = ''
        self.y_primary_axis_title = ''
        self.y_secondary_axis_title = ''
        self.title = ''
        self.primary_colours_palete = None
        self.secondary_colours_palete = None

    def __draw_graph_title(self):
        if self.title != '':
            point = Point(self.left_margin + (self.width / 2), self.top_margin - (self.top_margin / 3))
            self.svg_contents += svg_monkey.write_text(point, self.title, 0, 'title')

    def __draw_x_axis_title(self, rotated_labels = False):
        if self.x_axis.title != '':
            y_buffer = 60
            if rotated_labels == True:
                y_buffer += 95
            point = Point(self.left_margin + (self.width/2), self.top_margin + self.height + y_buffer)
            self.svg_contents += svg_monkey.write_text(point, self.x_axis.title, 0, 'axis_title')

    def __draw_y_axis_title(self, axis, offset = 75):
        if axis.title != '' and axis.title != None:
            point = Point(self.left_margin - offset, self.top_margin + (self.height/2))
            self.svg_contents += svg_monkey.write_text(point, axis.title, 270, 'axis_title')

    #WTF is this self referential thing?
    def __draw_x_axis(self):
        self.__draw_x_axis()

    def __draw_x_axis(self):
        start_point = Point(self.left_margin, self.top_margin + self.height)
        end_point = Point(self.left_margin + self.width, self.top_margin + self.height)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        rotated_labels = False
        if self.x_axis.markers != None:
            for counter in range(0, len(self.x_axis.markers) ):#-1
                start_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height)
                end_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 15)
                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                start_point = Point(self.left_margin -5 + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 30)
                rotation = 0
                y_position = self.top_margin + self.height + 30
                if str(self.x_axis.markers[counter].marker.label).find(' ') > -1:
                    if rotated_labels == False:
                        rotated_labels = True
                    rotation = 90
                    y_position = y_position + 45

                self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].marker.label),rotation,'x_axis_label')
                
        self.__draw_x_axis_title(rotated_labels)

    # def __draw_x_axis_for_int(self):
    #     start_point = Point(self.left_margin, self.top_margin + self.height)
    #     end_point = Point(self.left_margin + self.width, self.top_margin + self.height)
    #     self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #     if self.x_axis.markers != None:
    #         for counter in range(0, len(self.x_axis.markers)):
    #             start_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height)
    #             end_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 15)
    #             self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #             start_point = Point(self.left_margin -5 + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 30)
    #             self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].marker.label),0,'x_axis_label')
    #     self.__draw_x_axis_title()

    def __format_axis_label_for_date(self, value, format_value):
        if format_value is not None:
            return value.strftime(format_value)
        else:
            return str(value)


    # def __draw_x_axis_for_date(self):
    #     start_point = Point(self.left_margin, self.top_margin + self.height)
    #     end_point = Point(self.left_margin + self.width, self.top_margin + self.height)
    #     self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #     if self.x_axis.markers != None:
    #         for counter in range(0, len(self.x_axis.markers)-1):
    #             start_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height)
    #             end_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 15)
    #             self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #             start_point = Point(self.left_margin -5 + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 30)
    #             #self.svg_contents += svg_monkey.write_text(start_point, self.__format_axis_label_for_date(self.x_axis.markers[counter].marker.value, self.x_axis_format),0,'x_axis_label')
    #             self.svg_contents += svg_monkey.write_text(start_point, self.x_axis.markers[counter].marker.label, 0,'x_axis_label')
    #     self.__draw_x_axis_title()

    # def __draw_x_axis_for_datetime(self):
    #     start_point = Point(self.left_margin, self.top_margin + self.height)
    #     end_point = Point(self.left_margin + self.width, self.top_margin + self.height)
    #     self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #     rotated_labels = False
    #     if self.x_axis.markers != None:
    #         for counter in range(0, len(self.x_axis.markers)):
    #             start_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height)
    #             end_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 15)
    #             self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')
                
    #             rotation = 0
    #             y_position = self.top_margin + self.height + 30
    #             if str(self.x_axis.markers[counter].marker.label).find(' ') > -1:
    #                 if rotated_labels == False:
    #                     rotated_labels = True
    #                 rotation = 90
    #                 y_position = y_position + 45
                
    #             start_point = Point(self.left_margin -5 + (self.x_axis.markers[counter].percentile * self.width), y_position)
    #             self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].marker.label),rotation,'x_axis_label')
    #     self.__draw_x_axis_title(rotated_labels)

    # def __draw_x_axis_for_time_value(self):
    #     start_point = Point(self.left_margin, self.top_margin + self.height)
    #     end_point = Point(self.left_margin + self.width, self.top_margin + self.height)
    #     self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #     if self.x_axis.markers != None:
    #         for counter in range(0, len(self.x_axis.markers)):
    #             start_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height)
    #             end_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 15)
    #             self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #             start_point = Point(self.left_margin -5 + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 30)
    #             self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].marker.label),0,'x_axis_label')
    #     self.__draw_x_axis_title()

    # def __draw_x_axis_for_float(self):
    #     start_point = Point(self.left_margin, self.top_margin + self.height)
    #     end_point = Point(self.left_margin + self.width, self.top_margin + self.height)
    #     self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #     if self.x_axis.markers != None:
    #         for counter in range(0, len(self.x_axis.markers)):
    #             start_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height)
    #             end_point = Point(self.left_margin + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 15)
    #             self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

    #             start_point = Point(self.left_margin -5 + (self.x_axis.markers[counter].percentile * self.width), self.top_margin + self.height + 30)
    #             self.svg_contents += svg_monkey.write_text(start_point, str(self.x_axis.markers[counter].marker.label),0,'x_axis_label')
    #     self.__draw_x_axis_title()


    def __draw_y_axis(self, axis, axis_position, reverse = False):
        if axis is not None:
            if axis.data_type is int:
                self.__draw_y_axis_for_int(axis, axis_position, reverse)
            if axis.data_type is float:
                self.__draw_y_axis_for_float(axis, axis_position, reverse)
            if axis.data_type is datetime.date:
                self.__draw_y_axis_for_date(axis, axis_position, reverse)
            if axis.data_type is datetime.datetime:
                self.__draw_y_axis_for_datetime(axis, axis_position, reverse)
            if axis.data_type is TimeValue:
                self.__draw_y_axis_for_time_value(axis, axis_position, reverse)
    
    def __handle_reverse(self, reverse_axis, position, adjustment):
        if reverse_axis == True:
            return position + adjustment
        else:
            return position - adjustment

    def __new_draw_y_axis(self, axis, axis_position, reverse):
        start_point = Point(axis_position, self.top_margin + self.height)
        end_point = Point(axis_position, self.top_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        #REFACTOR AHOY!!
        css_label = 'y_axis_label'
        if reverse == True:
            css_label = css_label + '_reverse'

        if axis.markers != None:
            for counter in range(0, len(axis.markers)-1):
                start_point = Point(axis_position, (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                end_point = Point(self.__handle_reverse(reverse, axis_position, 15), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))

                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                #int
                label_point = Point(self.__handle_reverse(reverse, axis_position, 20), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str((axis.markers[counter].marker.label)), 0, css_label)

                #date
                label_point = Point(self.__handle_reverse(reverse, axis_position, 65), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, self.__format_axis_label_for_date(axis.markers[counter].marker.value, self.x_axis_format),0,'y_axis_label')

                #datetime
                label_point = Point(self.__handle_reverse(reverse, axis_position, 65), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(axis.markers[counter].marker.label),0,'y_axis_label')

                #timevalue
                label_point = Point(self.__handle_reverse(reverse, axis_position, 20), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(axis.markers[counter].marker.label),0,'y_axis_label')

                #float
                label_point = Point(self.__handle_reverse(reverse, axis_position, 20), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(axis.markers[counter].marker.label),0, css_label)

        self.__draw_y_axis_title(axis)


    def __draw_y_axis_for_int(self, axis, axis_position, reverse):
        start_point = Point(axis_position, self.top_margin + self.height)
        end_point = Point(axis_position, self.top_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        #REFACTOR AHOY!!
        css_label = 'y_axis_label'
        if reverse == True:
            css_label = css_label + '_reverse'

        if axis.markers != None:
            for counter in range(0, len(axis.markers)):#-1
                start_point = Point(axis_position, (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                end_point = Point(self.__handle_reverse(reverse, axis_position, 15), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))

                #print(axis.markers[counter].marker.label,axis.markers[counter].percentile, start_point.x, start_point.y)

                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                label_point = Point(self.__handle_reverse(reverse, axis_position, 20), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str((axis.markers[counter].marker.label)), 0, css_label)
        self.__draw_y_axis_title(axis)

    def __draw_y_axis_for_date(self, axis, axis_position, reverse):
        start_point = Point(axis_position, self.top_margin + self.height)
        end_point = Point(axis_position, self.top_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        if axis.markers != None:
            for counter in range(0, len(axis.markers)):
                start_point = Point(axis_position, (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                end_point = Point(self.__handle_reverse(reverse, axis_position, 15), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                label_point = Point(self.__handle_reverse(reverse, axis_position, 65), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, self.__format_axis_label_for_date(axis.markers[counter].marker.value, self.x_axis_format),0,'y_axis_label')
        self.__draw_y_axis_title(axis, 150)

    def __draw_y_axis_for_datetime(self, axis, axis_position, reverse):
        start_point = Point(axis_position, self.top_margin + self.height)
        end_point = Point(axis_position, self.top_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        if axis.markers != None:
            for counter in range(0, len(axis.markers)):
                start_point = Point(axis_position, (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                end_point = Point(self.__handle_reverse(reverse, axis_position, 15), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                label_point = Point(self.__handle_reverse(reverse, axis_position, 65), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(axis.markers[counter].marker.label),0,'y_axis_label')
        self.__draw_y_axis_title(axis, 150)

    def __draw_y_axis_for_time_value(self, axis, axis_position, reverse):
        start_point = Point(axis_position, self.top_margin + self.height)
        end_point = Point(axis_position, self.top_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        if axis.markers != None:
            for counter in range(0, len(axis.markers)):
                start_point = Point(axis_position, (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                end_point = Point(self.__handle_reverse(reverse, axis_position, 15), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                label_point = Point(self.__handle_reverse(reverse, axis_position, 20), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(axis.markers[counter].marker.label),0,'y_axis_label')
        self.__draw_y_axis_title(axis, 150)

    def __draw_y_axis_for_float(self, axis, axis_position, reverse):
        start_point = Point(axis_position, self.top_margin + self.height)
        end_point = Point(axis_position, self.top_margin)
        self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

        #refactor AHOY!
        css_label = 'y_axis_label'
        if reverse == True:
            css_label = css_label + '_reverse'

        if axis.markers != None:
            for counter in range(0, len(axis.markers) - 1):
                start_point = Point(axis_position, (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                end_point = Point(self.__handle_reverse(reverse, axis_position, 15), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height))
                
                self.svg_contents += svg_monkey.write_line(start_point, end_point, 'Black', 'axis')

                label_point = Point(self.__handle_reverse(reverse, axis_position, 20), (self.top_margin + self.height) - (axis.markers[counter].percentile * self.height) + 5)
                self.svg_contents += svg_monkey.write_text(label_point, str(axis.markers[counter].marker.label),0, css_label)
        self.__draw_y_axis_title(axis, 150)

    #there's a mismatch between axes and points >> and I think it's y_axis.high
    def __translate_data_to_points(self, data_set):
        y_axis = None
        if self.additional_axis_meta_data is None:
            y_axis = self.y_primary_axis
        else:
            if self.additional_axis_meta_data.get_axis_meta_data_item(data_set.name).axis_type == AxisType.PRIMARY:
                y_axis = self.y_primary_axis
            else:
                y_axis = self.y_secondary_axis

        points = []
        for data_item in data_set:
            x = self.left_margin + round((((data_item.key - self.x_axis.low) / (self.x_axis.high - self.x_axis.low)) * self.width),2)
            # if data_item.key == datetime.date(2020,8,9):

            #     print(data_item.key, x, self.left_margin, self.width)
            if data_item.value == 12256:
                monkey = "go"

            y = self.top_margin + round(self.height - ((((data_item.value - y_axis.low) / (y_axis.high - y_axis.low)) * self.height)), 2)
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
        elif raw_range.days > 31: #clunky
            #months
            return datetime.date(value.year, value.month, 1)
        else:
            #days
            return value

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
        if self.x_axis.data_type is int or self.x_axis.data_type is float:
            if self.x_axis.low > 0:
                self.x_axis.low = 0
        if self.y_primary_axis.data_type is int or self.y_primary_axis.data_type is float:
            if self.y_primary_axis.low > 0:
                self.y_primary_axis.low = 0
        if self.y_secondary_axis is not None:
            if self.y_secondary_axis.data_type is int or self.y_secondary_axis.data_type is float:
                if self.y_secondary_axis.low > 0:
                    self.y_secondary_axis.low = 0

    def __revise_high_low(self, axis):
        if axis.markers is not None:
            axis.low = axis.markers[0].marker.value
            axis.high = axis.markers[len(axis.markers)-1].marker.value

    def __determine_y_axes(self):
        lowest_primary_y_value = None
        highest_primary_y_value = None
        lowest_secondary_y_value = None
        highest_secondary_y_value = None

        for data_set in self.data_sets:

            lowest_y_value = data_set.get_lowest_value()
            highest_y_value = data_set.get_highest_value()

            if self.additional_axis_meta_data.get_axis_meta_data_item(data_set.name).axis_type == AxisType.PRIMARY:

                if lowest_primary_y_value is None:
                    lowest_primary_y_value = lowest_y_value
                else:
                    if lowest_y_value < lowest_primary_y_value:
                        lowest_primary_y_value = lowest_y_value

                if highest_primary_y_value is None:
                    highest_primary_y_value = highest_y_value
                else:
                    if highest_y_value > highest_primary_y_value:
                        highest_primary_y_value = highest_y_value

            elif self.additional_axis_meta_data.get_axis_meta_data_item(data_set.name).axis_type == AxisType.SECONDARY:

                if lowest_secondary_y_value is None:
                    lowest_secondary_y_value = lowest_y_value
                else:
                    if lowest_y_value < lowest_secondary_y_value:
                        lowest_secondary_y_value = lowest_y_value

                if highest_secondary_y_value is None:
                    highest_secondary_y_value = highest_y_value
                else:
                    if highest_y_value > highest_secondary_y_value:
                        highest_secondary_y_value = highest_y_value

        y_data_type, y_low, y_high = self.__evaluate_axis_data_by_type(lowest_primary_y_value, highest_primary_y_value)
        self.y_primary_axis = Axis(y_low, y_high, y_data_type)

        y_data_type, y_low, y_high = self.__evaluate_axis_data_by_type(lowest_secondary_y_value, highest_secondary_y_value)
        self.y_secondary_axis = Axis(y_low, y_high, y_data_type)

    def __determine_y_axis(self):
        lowest_y_value, highest_y_value = self.data_sets.get_lowest_and_highest_value()
        y_data_type, y_low, y_high = self.__evaluate_axis_data_by_type(lowest_y_value, highest_y_value)
        self.y_primary_axis = Axis(y_low, y_high, y_data_type)

    def __determine_x_axis(self):
        lowest_x_value, highest_x_value = self.data_sets.get_lowest_and_highest_key()
        #print(lowest_x_value, highest_x_value)
        x_data_type, x_low, x_high = self.__evaluate_axis_data_by_type(lowest_x_value, highest_x_value)
        self.x_axis = Axis(x_low, x_high, x_data_type)

    def __evaluate_data(self, zero_base = False, sort_data_sets = True):
        self.__determine_x_axis()

        if self.additional_axis_meta_data is None:
            self.__determine_y_axis()
        else:
            self.__determine_y_axes()

        if zero_base == True:
            self.__zero_base_for_int()

        self.__set_axis_markers(self.x_axis)
        self.__revise_high_low(self.x_axis)

        self.__set_axis_markers(self.y_primary_axis)
        self.__revise_high_low(self.y_primary_axis)
        if self.y_secondary_axis is not None:
            self.__set_axis_markers(self.y_secondary_axis)
            self.__revise_high_low(self.y_secondary_axis)

        if sort_data_sets == True:
            self.data_sets = sorted(self.data_sets)

    def __set_axis_markers(self, axis):
        creator = None

        if axis.data_type is int:
            creator = IntAxisLabelsCreator
        elif axis.data_type is float:
            creator = FloatAxisLabelsCreator
        elif axis.data_type is datetime.date:
            creator = DateAxisLabelsCreator #TECHDEBT: should set date format for label here as expressed in yaml file
        elif axis.data_type is datetime.datetime:
            creator = DateTimeAxisLabelsCreator
        elif axis.data_type is TimeValue:
            creator = TimeValueAxisLabelsCreator
            
        axis.markers = creator(axis.low, axis.high).axis_markers

    def __write_point_markers(self, points, display_markers=True, display_labels=True, color="", label = ""):
        point = None

        for point in points:
            if display_markers == True:
                self.svg_contents += svg_monkey.write_circle(point, 4, color)
        if display_labels == True:
            self.svg_contents += svg_monkey.write_text(Point(point.x + 10, point.y + 5), label, 0, 'legend_item', color)

    def __set_axes_titles(self):
        if self.x_axis != None:
            self.x_axis.title = self.x_axis_title
        if self.y_primary_axis != None:
            self.y_primary_axis.title = self.y_axis_title

    def __calculate_legend_svg_height(self):
        return len(self.data_sets) * 20

            

    def __build_legend_contents(self, left, primary_colours_palete, secondary_colours_palete):
        contents = ''
        
        #colours_palete = ColoursPalete(3)
        spacer = 20
        #left = self.left_margin + self.width + 50
        if self.additional_axis_meta_data is not None:
            left += 50
        #this is now handled with a separate method call (title and legend now different)
        #contents += svg_monkey.write_text(Point(left, self.top_margin), 'Legend', 0, 'legend_item_title')

        for data_set in self.data_sets: #sorted(self.data_sets):
            if data_set.axis_type == AxisType.PRIMARY:
                colours_palete = primary_colours_palete
            else:
                colours_palete = secondary_colours_palete

            colour = colours_palete.get_next_colour()
            contents += svg_monkey.write_line(Point(left - 30, spacer - 3), Point(left -10, spacer - 3), colour, None, str(data_set.id))
            contents += svg_monkey.write_text(Point(left, spacer), data_set.name, 0, 'legend_item', colour, str(data_set.id), 'onclick="highlight_lines(\'' + str(data_set.id) + '\');"')
            spacer += 20
        return contents

    def __set_graph_dimensions(self):
        self.bottom_margin = (1/5) * self.height
        self.top_margin = self.bottom_margin / 2
        self.left_margin = (1/10) * self.width
        self.right_margin = self.left_margin
        self.height = self.height - self.bottom_margin - self.top_margin
        self.width = self.width - self.left_margin - (self.right_margin * 0.4) #the last (bit in brackets) is to push the right hand side to a convenient point

    def draw_legend_title(self):
        self.svg_legend_title_contents = svg_monkey.write_svg_start(100, 60)
        self.svg_legend_title_contents += svg_monkey.write_text(Point(30, 50), 'Legend', 0, 'legend_item_title')
        self.svg_legend_title_contents += svg_monkey.write_svg_end()

    def draw_legend(self):
        self.svg_legend_contents = svg_monkey.write_svg_start(160, self.__calculate_legend_svg_height() + 10)
        self.svg_legend_contents += self.__build_legend_contents(30, copy.copy(self.primary_colours_palete), copy.copy(self.secondary_colours_palete))
        self.svg_legend_contents += svg_monkey.write_svg_end()

    def draw_graph(self, sort_data_sets = True):
        self.svg_contents = svg_monkey.write_svg_start(self.width, self.height)
        self.__set_graph_dimensions()

        self.__evaluate_data(True, sort_data_sets)    
        self.__draw_graph_title()
        self.__set_axes_titles()
        self.__draw_x_axis()
        self.__draw_y_axis(self.y_primary_axis, self.left_margin)
        self.__draw_y_axis(self.y_secondary_axis, self.left_margin + self.width, True)

        #primary_colours_palete = ColoursPalete(self.__get_data_set_count(self.data_sets, AxisType.PRIMARY), ColoursPalete.RGBAnchor.BLUE)
        self.primary_colours_palete = HSLColoursPalete(self.__get_data_set_count(self.data_sets, AxisType.PRIMARY))
        #secondary_colours_palete = ColoursPalete(self.__get_data_set_count(self.data_sets, AxisType.SECONDARY), ColoursPalete.RGBAnchor.RED)
        self.secondary_colours_palete = HSLColoursPalete(self.__get_data_set_count(self.data_sets, AxisType.SECONDARY))
        self.__draw_graph(copy.copy(self.primary_colours_palete), copy.copy(self.secondary_colours_palete))

        #this now replaced by below section building legend in separate SVG element
        #self.svg_contents += self.__build_legend_contents(self.left_margin + self.width + 50, copy.copy(self.primary_colours_palete), copy.copy(self.secondary_colours_palete))

        self.svg_contents += svg_monkey.write_svg_end()

        #LEGEND!!!
        self.draw_legend()
        self.draw_legend_title()

    def __get_data_set_count(self, data_sets, axis_type):
        data_set_counter = 0
        for data_set in data_sets:
            if data_set.axis_type == axis_type:
                data_set_counter += 1
        #print("Data Set Count", data_set_counter)
        return data_set_counter

    def __draw_graph(self, primary_colours_palete, secondary_colours_palete):
        for data_set in self.data_sets: #sorted(self.data_sets): #self.data_sets:
            if data_set.axis_type == AxisType.PRIMARY:
                colours_palete = primary_colours_palete
            else:
                colours_palete = secondary_colours_palete

            colour = colours_palete.get_next_colour()
            points = self.__translate_data_to_points(data_set)
            self.svg_contents += svg_monkey.write_lines(points, colour, str(data_set.id),'onmouseover="highlight_legend(\'' + str(data_set.id) + '\');" onmouseout="highlight_legend(\'' + str(data_set.id) + '\');"')
            self.__write_point_markers(points, False, False, colour, data_set.name)



