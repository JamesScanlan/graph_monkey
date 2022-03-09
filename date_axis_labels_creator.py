import datetime
from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator
from axis_markers import AxisMarkers
from axis_marker import AxisMarker

class DateAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high, format, padding):
        super().__init__(low, high, format, padding)
        self.__create_axis_markers()

    def __deterimine_interval(self, reference_date, date_range):
        interval = "Day"
        if date_range.days > self.__get_days_in_year(reference_date.year):
            if date_range.days > (365 * 2):
                interval = "Year"
            else:
                interval = "Month"
        elif date_range.days > (self.__get_days_in_month(reference_date)) * 2:
            interval = "Month"
        elif date_range.days > 15:
            interval = "Week"
        return interval

    def __determine_interval_date_for_year_increment(self, reference_date):
        return datetime.date(reference_date.year + 1, 1, 1)
        
    def __determine_interval_date_for_month_increment(self, reference_date):
        calculated_month = reference_date.month
        calculated_year = reference_date.year

        if reference_date.month == 12:
            calculated_month = 1
            calculated_year += 1
        else:
            calculated_month += 1

        return datetime.date(calculated_year, calculated_month, 1)

    def __determine_interval_date_for_week_increment(self, reference_date):
        calculated_day = reference_date.day
        calculated_month = reference_date.month
        calculated_year = reference_date.year

        days_in_month = self.__get_days_in_month(reference_date)

        if calculated_day + 7 > days_in_month:
            calculated_day = 7 - (days_in_month - calculated_day)
            if calculated_month == 12:
                calculated_month = 1
                calculated_year += 1
            else:
                calculated_month +=1
        else:
            calculated_day = calculated_day + 7
        return datetime.date(calculated_year, calculated_month, calculated_day)

    def __determine_interval_date_for_day_increment(self, reference_date):
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
                calculated_day = 1
                if reference_date.month == 12:
                    calculated_month = 1
                    calculated_year +=1
                else:
                    calculated_month +=1
            else:
                calculated_day += 1
        
        return datetime.date(calculated_year, calculated_month, calculated_day)

    def __get_next_interval_date(self, reference_date, interval):
        if interval == "Day":
            return self.__determine_interval_date_for_day_increment(reference_date)
        elif interval == "Month":
            return self.__determine_interval_date_for_month_increment(reference_date)
        elif interval =="Week":
            return self.__determine_interval_date_for_week_increment(reference_date)
        else:
            return self.__determine_interval_date_for_year_increment(reference_date)

    def __calculate_date_percentile(self, date_value, calculated_maximum):
        low = self.low.toordinal()
        high = calculated_maximum.toordinal()
        value = date_value.toordinal()
        return (value - low) / (high - low)

    def __get_calculated_high_based_on_next_interval_date(self, start_date, interval):
        current_day = start_date
        exit_loop = False
        while exit_loop == False:
            increment_date = self.__get_next_interval_date(current_day, interval)
            current_day = increment_date
            if increment_date > self.high or increment_date == self.high:
                exit_loop = True
                
        return current_day
        

    def __create_axis_markers(self):
        interval = self.__deterimine_interval(self.low, self.high - self.low)
        current_day = self.low
        maximum_day = self.high
        #changed to be highest data value...not the a future logical calendar date like 1st of week, month or year
        #maximum_day = self.__get_calculated_high_based_on_next_interval_date(current_day, interval)
        new_axis_markers = AxisMarkers()

        #Stop first one being created
        #axis_label = AxisLabel(current_day, current_day.strftime("%d/%m/%Y"))
        #axis_percentile = self.__calculate_date_percentile(current_day, maximum_day)
        #new_axis_markers.add_axis_marker(AxisMarker(axis_label, axis_percentile))        
        
        exit_loop = False
        while exit_loop == False:
            increment_date = self.__get_next_interval_date(current_day, interval)

            axis_label = AxisLabel(increment_date, increment_date.strftime("%d/%m/%Y"))

            axis_percentile = self.__calculate_date_percentile(increment_date, maximum_day)

            new_axis_markers.add_axis_marker(AxisMarker(axis_label, axis_percentile))
            
            if increment_date >= self.high: # or increment_date == self.high:
                exit_loop = True
            else:
                current_day = increment_date

        #self.__display_axis_labels()

        self.axis_markers = new_axis_markers


    def __display_axis_labels(self):
        for axis_marker in self.axis_markers: #ah yes it currently isn't iteratable
            if axis_marker != None:
                print(axis_marker)
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


