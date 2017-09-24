PRESET_DAYS = ['M', 'Tu', 'W', 'Th', 'F']
from datetime import datetime, date
from datetime import time as time

class TimeInterval:
    """
    Expects day_col formatted as combinations of PRESET_DAYS
    Expects time_col formatted as TIME + a/p + - + TIME + a/p
    """

    def __init__(self, day_col, time_col):
        self.sanitize_inputs(day_col, time_col)

    def sanitize_inputs(self, day_col, time_col):
        if day_col:
            self.days = self.get_days(day_col)
        if time_col:
            self.times = self.get_times(time_col)

    def get_days(self, day_list):
        ret_days = []
        for day in PRESET_DAYS:
            if day in day_list:
                ret_days.append(day)
        return ret_days

    def get_times(self, time_col):
        if time_col.find('-') == -1:
            return []
        ret_times = []
        for b_time in time_col.split('-'):
            b_time += 'm'
            g_time = datetime.strptime(b_time, '%I:%M%p')
            ret_times.append(g_time)
        return ret_times

    def overlaps_times_and_days(self, other):
        for day in self.days:
            if day in other.days:
                if self.overlaps_times(other):
                    return True
        return False

    def overlaps_times(self, other):
        my_start = self.times[0]
        my_end = self.times[1]

        other_start = other.times[0]
        other_end = other.times[1]

        return (other_start <= my_start <= other_end) or (my_start <= other_start <= my_end)

    def inside_time(self, other):
        try:
            my_start = self.times[0]
            my_end = self.times[1]

            other_start = other.times[0]
            other_end = other.times[1]
        except IndexError as e:
            return False
        return (other_start <= my_start <= other_end) and (other_start <= my_end <= other_end) or \
               (my_start <= other_start <= my_end) and (my_start <= other_end <= my_end)


    def distance_from(self, other):
        my_start = self.times[0]
        my_end = self.times[1]

        other_start = other.times[0]
        other_end = other.times[1]

        one = abs((my_start - other_end)).total_seconds()/3600
        two = abs((my_end - other_start).total_seconds()/3600)

        return min(6, min(one, two))


class DefaultTimeInterval(TimeInterval):
    def __init__(self):
        super().__init__(None, None)
        self.days = []
        self.times = []

    def overlaps_times(self, other):
        return False

    def overlaps_times_and_days(self, other):
        return False

    def distance_from(self, other):
        return 1

