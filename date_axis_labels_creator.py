import datetime
from axis_label import AxisLabel
from axis_labels_creator import AxisLabelsCreator

class DateAxisLabelsCreator(AxisLabelsCreator):

    def __init__(self, low, high):
        super().__init__(low, high)
        self.__set_axis_labels()
        #self.__display_axis_labels()

    def __deterimine_interval(self, reference_date, date_range):
        interval = "Day"
        if date_range.days > self.__get_days_in_year(reference_date.year):
            interval = "Year"
        elif date_range.days > self.__get_days_in_month(reference_date):
            interval = "Month"
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
        else:
            return self.__determine_interval_date_for_year_increment(reference_date)

    def __set_axis_labels(self):
        date_range = self.high - self.low
        interval = self.__deterimine_interval(self.low, date_range)

        current_day = self.low

        axis_labels = []
        axis_labels.append(AxisLabel(current_day, current_day.strftime("%d/%m/%Y")))
        
        exit_loop = False
        while exit_loop == False:
            increment_date = self.__get_next_interval_date(current_day, interval)

            axis_labels.append(AxisLabel(increment_date, increment_date.strftime("%d/%m/%Y")))
            
            if increment_date > self.high or increment_date == self.high:
                exit_loop = True
            else:
                current_day = increment_date

        self.axis_labels = axis_labels

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


