from datetime import datetime, date
from datetime import time as time
from collections import namedtuple

DAY_INDEX = 0
TIME_INDEX = 1
PRESET_DAYS = ['M', 'Tu', 'W', 'Th', 'F', ' ']
DayTime = namedtuple(typename='DayTime', field_names='day times')
TimeInterval = namedtuple(typename='TimeInterval', field_names='start_time end_time')


class TimeIntervalCollection:
    """
    Expects day_col formatted as combinations of PRESET_DAYS
    Expects time_col formatted as TIME + a/p + - + TIME + a/p
    """

    def __init__(self, day_col, time_col):
        self.days = []
        self.times = []
        self.day_time_pairs = []
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

            self.day_time_pairs = self.get_day_time_pairs(self.days, self.times)
        except ValueError:
            raise ValueError('The input time is not in the correct format!')

    @staticmethod
    def get_day_time_pairs(days, times):
        """
        Will 'pair' up the days and their corresponding times. It does this by
        working with the assumption that there are only three cases -
        Where the number of days is equal to the number of times:
            In that case just spread acoordingly
        Where the number of days is greater than the number of times (PHYS one lecture three days):
            In that case use all the times up and then give the last time to the
            remaining days
        Where the number of days is less than the number of times (Two lectures one day):
            In that case use all the days up and then give the last times to the remaining
            days.
        :param days: The list of days to be spread
        :param times: The list of times to be spread
        :return: The correct pairs between times and days
        """
        ret_pairs = []
        day_len = len(days)
        time_len = len(times)
        # If one is empty just return
        if day_len == 0 or time_len == 0:
            return []
        if day_len == time_len:
            # Split them up if they are equal
            for i in range(0, day_len):
                ret_pairs.append(DayTime(days[i], times[i]))
            return ret_pairs
        elif day_len > time_len:
            time_count = 0
            for day in days:
                if day == ' ':
                    time_count += 1
                else:
                    ret_pairs.append(DayTime(day, times[time_count]))
            return ret_pairs
        else:
            # Distribute all days
            for i in range(0, day_len):
                ret_pairs.append(DayTime(days[i], times[i]))
            # Give remaining times the last day
            for i in range(day_len, time_len):
                ret_pairs.append(DayTime(days[day_len - 1], times[i]))
            return ret_pairs

    @staticmethod
    def get_days(day_list):
        """
        Takes in a day string and converts it into an array of days.
        Converting data into usable format.
        :param day_list: In the form MWF M, etc.
        :return: an array of days
        """
        unsorted_days = []
        ret_days = [None] * len(day_list)

        # Check if preset days inside the day string
        for day in PRESET_DAYS:
            if day in day_list:
                # Check how many days inside the day string and add them
                for i in range(0, day_list.count(day)):
                    unsorted_days.append(day)

        # Based off the idea of counting sort
        # Sort the days based on how early they appear inside the string
        for i in range(0, len(unsorted_days)):
            # Set the index
            index = day_list.index(unsorted_days[i])
            # If it is there, choose the index after the first one
            if ret_days[index]:
                index = day_list.index(unsorted_days[i], index + 1)
            # Put the unsorted day in its correct location
            ret_days[index] = unsorted_days[i]
        # Removing extra Nones from the array if there happen to be any
        ret_days = [x for x in ret_days if x is not None]
        return ret_days

    @staticmethod
    def get_times(time_col):
        """
        Convert time string into Python time object. Should be given in the form TIMEa-TIMEp
        Ex: 8:00a-12:00p. Will fix to be more flexible later.
        :param time_col: The input time string
        :return: An array of named tuples Time Intervals
        """
        # If it is not in that usable form return nothing
        if time_col.find('-') == -1:
            return []

        ret_times = []
        # Look for time strings split by space in case given a string with multiple intervals
        t_intervals = time_col.split(' ')

        # Check each interval
        for t_interval in t_intervals:
            # Find the hours split by '-'
            # Adding to a list here to make a real interval
            temp_time_storage = []
            for hour_time in t_interval.split('-'):
                # Add 'm' to convert it to Python recognizable format
                hour_time += 'm'
                formatted_interval = datetime.strptime(hour_time, '%I:%M%p')
                # Add the interval to the returned interval
                temp_time_storage.append(formatted_interval)
            # Add interval to the list of intervals
            # Using named tuple here for readability
            time_interval = TimeInterval(temp_time_storage[0], temp_time_storage[1])
            ret_times.append(time_interval)
        return ret_times

    @staticmethod
    def overlaps_times_and_days(self, other):
        """
        Takes in two time interval collection objects and checks if they overlap
        times and days.
        :param self: One time interval
        :param other: The other time interval
        :return: True if they do overlap times and days, and False if they do not
        """
        for day_time_pair in self.day_time_pairs:
            for other_day_time_pair in other.day_time_pairs:
                # Checking if the days overlap
                # Days are stored at index 0 in day_time_pair
                if day_time_pair[DAY_INDEX] == other_day_time_pair[DAY_INDEX]:
                    if TimeIntervalCollection.overlaps_time_intervals(day_time_pair[TIME_INDEX],
                                                                      other_day_time_pair[TIME_INDEX]):
                        return True
        return False

    @staticmethod
    def overlaps_time_intervals(self_time, other_time):
        """
        Takes in two time interval named tuples and returns if they overlap time intervals.
        :param self_time: The first time interval
        :param other_time: The other time interval
        :return: True if they overlap and False if they do not
        """
        try:
            my_start = self_time[0]
            my_end = self_time[1]

            other_start = other_time[0]
            other_end = other_time[1]
        except IndexError:
            # If there is a failure of the named tuple return False by default
            return False
        # Check if it contained within the time interval
        if (other_start <= my_start <= other_end) or (my_start <= other_start <= my_end):
            return True
        return False

    """
    Check if a time interval is inside of another.
    """

    @staticmethod
    def inside_time(self, other):
        """
        Checks if the two time intervals are in inside each other.
        Expects two time interval named tuples.
        :param self: The first time interval
        :param other: The second time interval
        :return: True if one interval is contained within the other
        """
        try:
            # Using named tuple fields

            my_start = self.start_time
            my_end = self.end_time

            other_start = other.start_time
            other_end = other.end_time
        except IndexError:
            return True
        return (other_start <= my_start <= other_end) and (other_start <= my_end <= other_end) or \
               (my_start <= other_start <= my_end) and (my_start <= other_end <= my_end)

    @staticmethod
    def distance_from(self, other):
        """
        Finds the distance between two intervals in hours.
        Expects two time interval named tuples.
        :param self: One time interval
        :param other: The other time interval
        :return: The distance between them in minutes
        """
        my_start = self.start_time
        my_end = self.end_time

        other_start = other.start_time
        other_end = other.end_time

        one = abs((my_start - other_end)).total_seconds() / 3600
        two = abs((my_end - other_start).total_seconds() / 3600)

        # Using mins so it doesn't go out of control
        return max(1, min(6, min(one, two)))

    def __str__(self):
        return str(self.times[0]) + ', ' + str(self.times[1])


class DefaultTimeIntervalCollection(TimeIntervalCollection):
    """
    Just a default time interval class so that any class with no interval will just default to true
    for all methods. Basically represents something that can be done anytime.
    """

    def __init__(self):
        super().__init__(None, None)
        self.days = []
        self.times = []
