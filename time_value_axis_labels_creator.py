from time_value import TimeValue
from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator
from axis_markers import AxisMarkers
from axis_marker import AxisMarker

class TimeValueAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high):
        super().__init__(low, high)
        self.__create_axis_markers()
        #self.__set_axis_labels()
        #self.__display_axis_labels()

    def __deterimine_interval(self, reference_time, time_range):
        interval = 'Minute'
        if time_range.seconds > (60 * 60):
            interval = "Hour"
        return interval

    def __determine_interval_for_minute_increment(self, reference_datetime):

        calculated_hour = reference_datetime.hour
        calculated_minute = reference_datetime.minute
                
        if calculated_minute == 59:
            calculated_minute = 0
            calculated_hour += 1

            if calculated_hour > 23:
                calculated_hour =0 

        else:
            calculated_minute += 1
        
        return TimeValue(calculated_hour, calculated_minute)

    def __determine_interval_for_hour_increment(self, reference_datetime):

        calculated_hour = reference_datetime.hour
        calculated_minute = reference_datetime.minute
                
        calculated_hour += 1
        
        return TimeValue(calculated_hour, calculated_minute)


    def __get_next_interval_time_value(self, reference_datetime, interval):
        if interval == "Minute":
            return self.__determine_interval_for_minute_increment(reference_datetime)
        elif interval == "Hour":
            return self.__determine_interval_for_hour_increment(reference_datetime)
         

    # def __set_axis_labels(self):
    #     time_range = self.high - self.low
    #     interval = self.__deterimine_interval(self.low, time_range)

    #     current_time_value = self.low

    #     axis_labels = []
    #     axis_labels.append(AxisLabel(current_time_value, str(current_time_value)))
        
    #     exit_loop = False
    #     while exit_loop == False:
    #         increment_time_value = self.__get_next_interval_time_value(current_time_value, interval)

    #         axis_labels.append(AxisLabel(increment_time_value, str(increment_time_value)))
            
    #         if increment_time_value > self.high or increment_time_value == self.high:
    #             exit_loop = True
    #         else:
    #             current_time_value = increment_time_value

    #     self.axis_labels = axis_labels

    def __calculate_time_value_percentile(self, timevalue):
        low = self.low.total_minutes()
        high = self.high.total_minutes()
        value = timevalue.total_minutes()
        return (value - low) / (high - low)

    def __create_axis_markers(self):
        interval = self.__deterimine_interval(self.low, self.high - self.low)

        current_time_value = self.low

        new_axis_markers = AxisMarkers()

        axis_label = AxisLabel(current_time_value, str(current_time_value))
        axis_percentile = self.__calculate_time_value_percentile(current_time_value)
        new_axis_markers.add_axis_marker(AxisMarker(axis_label, axis_percentile))  

        exit_loop = False
        while exit_loop == False:
            increment_time_value = self.__get_next_interval_time_value(current_time_value, interval)
            
            axis_label = AxisLabel(increment_time_value, str(increment_time_value))
            axis_percentile = self.__calculate_time_value_percentile(increment_time_value)
            new_axis_markers.add_axis_marker(AxisMarker(axis_label, axis_percentile))

            if increment_time_value > self.high or increment_time_value == self.high:
                exit_loop = True
            else:
                current_time_value = increment_time_value

        self.axis_markers = new_axis_markers

    def __display_axis_labels(self):
        for axis_label in self.axis_labels:
            if axis_label != None:
                print(axis_label.value, axis_label.label)
            else:
                print("None")




