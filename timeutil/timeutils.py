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

    """
    Make sure time_col and day_col is in the correct format, otherwise will throw a
    ValueError.
    """
    def sanitize_inputs(self, day_col, time_col):
        try:
            if day_col:
                self.days = self.get_days(day_col)
            if time_col:
                self.times = self.get_times(time_col)
        except ValueError:
            raise ValueError('The input time is not in the correct format!')

    """
    Convert days string into a usable data form.
    """
    def get_days(self, day_list):
        ret_days = []
        for day in PRESET_DAYS:
            if day in day_list:
                ret_days.append(day)
        return ret_days

    """
    Convert time string into Python time object. Should be given in the form TIMEa-TIMEp
    Ex: 8:00a-12:00p. Will fix to be more flexible later.
    """
    def get_times(self, time_col):
        # If it is not in that usable form return nothing
        if time_col.find('-') == -1:
            return []

        ret_times = []
        # Look for time strings split by space in case given a string with multiple intervals
        t_intervals = time_col.split(' ')

        # Check each interval
        for t_interval in t_intervals:
            # Find the hours split by '-'
            for hour_time in t_interval.split('-'):
                # Add 'm' to convert it to Python recognizable format
                hour_time += 'm'
                formatted_interval = datetime.strptime(hour_time, '%I:%M%p')
                # Add the interval to the returned interval
                # Just add the intervals together to a list, not keep them together
                ret_times.append(formatted_interval)
        return ret_times

    """
    Check if times and days overlap.
    """
    def overlaps_times_and_days(self, other):
        for day in self.days:
            if day in other.days:
                if self.overlaps_time(other):
                    return True
        return False

    """
    Check if two time intervals overlap each other.
    """
    def overlaps_time(self, other):
        try:
            my_start = self.times[0]
            my_end = self.times[1]

            other_start = other.times[0]
            other_end = other.times[1]
        except IndexError as e:
            return False
        return (other_start <= my_start <= other_end) or (my_start <= other_start <= my_end)

    """
    Check if a time interval is inside of another.
    """
    def inside_time(self, other):
        try:
            my_start = self.times[0]
            my_end = self.times[1]

            other_start = other.times[0]
            other_end = other.times[1]
        except IndexError as e:
            return True
        return (other_start <= my_start <= other_end) and (other_start <= my_end <= other_end) or \
               (my_start <= other_start <= my_end) and (my_start <= other_end <= my_end)

    """
    Find the distance between two intervals.
    This method is probably wrong.
    """
    def distance_from(self, other):
        my_start = self.times[0]
        my_end = self.times[1]

        other_start = other.times[0]
        other_end = other.times[1]

        one = abs((my_start - other_end)).total_seconds() / 3600
        two = abs((my_end - other_start).total_seconds() / 3600)

        return max(1, min(6, min(one, two)))

    def __str__(self):
        return str(self.times[0]) + ', ' + str(self.times[1])

"""
Just a default time interval class so that any class with no interval will just default to true
for all methods. Basically represents something that can be done anytime.
"""


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
