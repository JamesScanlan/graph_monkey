import datetime

class TimeValue(object):
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def total_minutes(self):
        return (self.hour * 60) + self.minute

    def __sub__(self, other_time_value):
        self_as_minutes = self.total_minutes()
        other_as_minutes = other_time_value.total_minutes()
        result = self_as_minutes - other_as_minutes 
        return datetime.timedelta(minutes = result)

    def __str__(self):
        return self.__double_digit_format(self.hour) + ":" + self.__double_digit_format(self.minute)

    def __lt__(self, other_time_value):
        return self.total_minutes() < other_time_value.total_minutes()

    def __gt__(self, other_time_value):
        return self.total_minutes() > other_time_value.total_minutes()

    def __eq__(self, other_time_value):
        if other_time_value == None:
            return False
        return self.total_minutes() == other_time_value.total_minutes()

    def __double_digit_format(self, value):
        if int(value) < 10:
            return '0' + str(value)
        else:
            return str(value)