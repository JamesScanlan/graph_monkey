import datetime
from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator
from axis_markers import AxisMarkers
from axis_marker import AxisMarker

class DateTimeAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high, format, padding):
        super().__init__(low, high, format, padding)
        self.__create_axis_markers()

    def __deterimine_interval(self, reference_datetime, datetime_range):
        interval = "Day"
        if datetime_range.days == 0:
            if datetime_range.seconds > (60 * 60):
                interval = "Hour"
            else:
                interval = "Minute"
        else:
            if datetime_range.days > self.__get_days_in_year(reference_datetime.year):
                interval = "Year"
            elif datetime_range.days > self.__get_days_in_month(reference_datetime):
                interval = "Month"
        return interval

    def __determine_interval_for_year_increment(self, reference_date):
        return datetime.date(reference_date.year + 1, 1, 1)
        
    def __determine_interval_for_month_increment(self, reference_date):
        calculated_month = reference_date.month
        calculated_year = reference_date.year

        if reference_date.month == 12:
            calculated_month = 1
            calculated_year += 1
        else:
            calculated_month += 1

        return datetime.date(calculated_year, calculated_month, 1)

    def __determine_interval_for_day_increment(self, reference_date):
        calculated_day = reference_date.day
        calculated_month = reference_date.month
        calculated_year = reference_date.year

        if reference_date.month in (4,5,6,11):
            if reference_date.day == 30:
                calculated_day = 1
                if reference_date.month == 12:
                    calculated_month = 1
                    calculated_year += 1
                else:
                    calculated_month +=1
            else:
                calculated_day += 1

        elif reference_date.month == 2:
            if reference_date.day == self.__get_days_in_february(reference_date.year):
                calculated_day = 1
                calculated_month = 3
            else:
                calculated_day += 1

        else:
            if reference_date.day == 31:
                current_day = 1
                if reference_date.month == 12:
                    calculated_month = 1
                    calculated_year +=1
                else:
                    calculated_month +=1
            else:
                calculated_day += 1
        
        return datetime.datetime(calculated_year, calculated_month, calculated_day, reference_date.hour, reference_date.minute)

    def __determine_interval_for_minute_increment(self, reference_datetime):

        calculated_year = reference_datetime.year
        calculated_month =reference_datetime.month
        calculated_day = reference_datetime.day

        calculated_hour = reference_datetime.hour
        calculated_minute = reference_datetime.minute
                
        if calculated_minute == 59:
            calculated_minute = 0
            calculated_hour += 1

            if calculated_hour > 23:
                calculated_day += 1
                calculated_hour =0 

            if calculated_month in (4,6,9,11):
                if calculated_day > 30:
                    calculated_day = 1
                    calculated_month +1
            elif calculated_month == 2:
                if self.__is_leap_year(calculated_year):
                    ref_day = 29
                else:
                    ref_day = 28
                if calculated_day > ref_day:
                    calculated_day = 1
                    calculated_month = 3
            else:
                if calculated_day > 31:
                    calculated_day = 1
                    calculated_month += 1

            if calculated_month > 12:
                calculated_month = 1

        else:
            calculated_minute += 1
        
        return datetime.datetime(calculated_year, calculated_month, calculated_day, calculated_hour, calculated_minute)

    def __determine_interval_for_hour_increment(self, reference_datetime):

        calculated_year = reference_datetime.year
        calculated_month =reference_datetime.month
        calculated_day = reference_datetime.day

        calculated_hour = reference_datetime.hour
        calculated_minute = reference_datetime.minute
                
        if calculated_hour >= 23:
            calculated_day += 1
            calculated_hour =0 

            if calculated_month in (4,6,9,11):
                if calculated_day > 30:
                    calculated_day = 1
                    calculated_month +1
            elif calculated_month == 2:
                if self.__is_leap_year(calculated_year):
                    ref_day = 29
                else:
                    ref_day = 28
                if calculated_day > ref_day:
                    calculated_day = 1
                    calculated_month = 3
            else:
                if calculated_day > 31:
                    calculated_day = 1
                    calculated_month += 1

            if calculated_month > 12:
                calculated_month = 1

        else:
            calculated_hour += 1
        
        return datetime.datetime(calculated_year, calculated_month, calculated_day, calculated_hour, calculated_minute)


    def __get_next_interval_datetime(self, reference_datetime, interval):
        if interval == "Minute":
            return self.__determine_interval_for_minute_increment(reference_datetime)
        elif interval == "Hour":
            return self.__determine_interval_for_hour_increment(reference_datetime)
        elif interval == "Day":
            return self.__determine_interval_for_day_increment(reference_datetime)
        elif interval == "Month":
            return self.__determine_interval_for_month_increment(reference_datetime)
        else:
            return self.__determine_interval_for_year_increment(reference_datetime)

    def __calculate_datetime_percentile(self, datetime_value):
        low = self.low.timestamp()
        high = self.high.timestamp()
        value = datetime_value.timestamp()
        return (value - low) / (high - low)


    def __create_axis_markers(self):
        interval = self.__deterimine_interval(self.low, self.high - self.low)
        current_datetime = self.low

        new_axis_markers = AxisMarkers()

        axis_label = AxisLabel(current_datetime, current_datetime.strftime(self.format))
        axis_percentile = self.__calculate_datetime_percentile(current_datetime)
        new_axis_markers.add_axis_marker(AxisMarker(axis_label, axis_percentile))

        exit_loop = False
        while exit_loop == False:
            increment_datetime = self.__get_next_interval_datetime(current_datetime, interval)

            axis_label = AxisLabel(increment_datetime, increment_datetime.strftime(self.format))
            axis_percentile = self.__calculate_datetime_percentile(increment_datetime)
            new_axis_markers.add_axis_marker(AxisMarker(axis_label, axis_percentile))
            
            if increment_datetime > self.high or increment_datetime == self.high:
                exit_loop = True
            else:
                current_datetime = increment_datetime

        self.axis_markers = new_axis_markers

    def __display_axis_labels(self):
        for axis_label in self.axis_labels:
            if axis_label != None:
                print(axis_label.value, axis_label.label)
            else:
                print("None")

    def __get_days_in_year(self, year):
        if self.__is_leap_year(year) == True:
            return 366
        else:
            return 365

    def __get_days_in_month(self, reference_date):
        if reference_date.month in (4,5,6,11):
            return 30
        elif reference_date.month == 2:
            return self.__get_days_in_february(reference_date.year)
        else:
            return 31

    def __is_leap_year(self, year):
        if year % 4 == 0:
            return True
        elif year % 100 == 0 and year % 400 == 0:
            return True
        else:
            return False

    def __get_days_in_february(self, year):
        if self.__is_leap_year(year) == True:
            return 29
        else:
            return 28


