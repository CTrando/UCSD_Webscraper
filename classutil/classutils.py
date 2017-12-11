from timeutil.timeutils import *

"""
Has a dictionary of subclasses. At the moment, new class types must be hardcoded in as follows.
This class is the big superclass controller of all the subclasses.
"""


class Class:
    def __init__(self, cursor, ID):
        # Initialize class by looking at its data
        self.cursor = cursor
        cursor.execute("SELECT * FROM DATA WHERE ROWID = ?", (ID,))

        # Setting the data dict to the database info
        self.data = dict(cursor.fetchone())

        self.subclasses = {}
        self.final = None

        for subclass_key in self.data:
            if 'KEY' not in subclass_key:
                continue
            subclass = self.data[subclass_key]
            if subclass:
                self.subclasses[subclass_key] = Subclass(cursor, self.data[subclass_key])

    def is_valid(self, w_set):
        """
        Return if the classes overlap. Will add more arguments in the future.

        :param w_set the set of classes (not subclasses) we are working with currently
        :return true if valid and false if not
        """

        if len(w_set) == 0:
            return True
        else:
            for choice in w_set:
                # TODO BIG BUG HERE MUST FIX SO FINALS DON'T OVERLAP
                # Checking with classes not subclasses
                if self.overlaps_times_and_days(choice):
                    return False
            return True

    def overlaps_time(self, choice_time):
        """
        Returns if every subclass in this class overlaps the time interval.

        :param choice_time the time to be compared
        :return true if every class in the class is partially inside the interval
        """

        for subclass in self.subclasses.values():
            # Return false if any do not overlap
            if not subclass.overlaps_time(choice_time):
                return False

        # Returns if every class overlaps
        return True

    def overlaps_times_and_days(self, choice):
        """
        Takes in two classes and returns whether their times overlap.
        :param choice: The other class
        :return: Whether the two classes overlap
        """

        for self_cl in self.subclasses.values():
            for choice_cl in choice.subclasses.values():
                if self_cl.overlaps_times_and_days(choice_cl):
                    return True
        return False

    def inside_time(self, choice_time):
        """
        Check if all subclasses of a class is inside a time interval.
        :param choice_time: The time interval to be compared
        :return: True if all subclasses are contained within the interval.
        """

        for subclass in self.subclasses.values():
            if not subclass.inside_time(choice_time):
                return False
        return True

    def distance_from_interval(self, interval):
        """
        Will add up the distances of all subclasses from the intervals.
        :param interval: The interval to be compared to
        :return: The cumulative distance from the interval
        """
        dist = 0
        for subclass in self.subclasses.values():
            dist += subclass.distance_from_interval(interval)
        return dist

    def earlier_time(self, interval):
        for subclass in self.subclasses.values():
            if subclass.earlier_time(interval):
                return True
        return False

    def __str__(self):
        """
        To string method for the class
        :return: Returns the to string of all the subclasses combined
        """
        ret = ''
        for cl in self.subclasses.values():
            ret += ' ' + str(cl)
        return ret


"""
Puts data into readable format given a table row.
"""


class Subclass:
    def __init__(self, cursor, ID):
        # Initialize class based on which table
        self.cursor = cursor
        cursor.execute("SELECT * FROM CLASSES WHERE ROWID = ?", (ID,))

        # Setting data
        self.data = dict(cursor.fetchone())

        # Initializing lecture type
        self.type = None
        if 'TYPE' in self.data:
            self.type = self.data['TYPE']

        # Default interval in case it is a final or is formatted strangely
        self.interval = DefaultTimeIntervalCollection()
        self.make_interval()

    """
    The class must not be a final (class type) and have a type. Unfortunately that means finals can overlap,
    which can cause problems - will fix later
    """

    def make_interval(self):
        # Check if type exists
        if not self.type:
            return
        # Check if type is not a final
        if self.type == 'FINAL':
            return

        if 'DAYS' in self.data and 'TIME' in self.data:
            interval = TimeIntervalCollection(self.data['DAYS'], self.data['TIME'])
            # Make sure that the interval has valid times
            if len(interval.times) > 0:
                self.interval = interval

    def is_in_days(self, str_days):
        return self.data['DAYS'] in str_days

    def overlaps_times_and_days(self, other):
        return TimeIntervalCollection.overlaps_times_and_days(self.interval, other.interval)

    def inside_time(self, other):
        for self_time in self.interval.times:
            for other_time in other.times:
                if not TimeIntervalCollection.inside_time(self_time, other_time):
                    return False
        return True

    def overlaps_time(self, other):
        """
        Expects a time interval and sees if the class times overlap.
        :param other: A time interval
        :return: True if they do overlap and false if they don't
        """
        for self_time in self.interval.times:
            for other_time in other.times:
                if TimeIntervalCollection.overlaps_time_intervals(self_time, other_time):
                    return True
        return False

    def distance_from_interval(self, other):
        """
        Expects another time interval object.
        :param other: The other time interval object to be compared
        :return: The distance from self's time interval to other's time interval
        """
        cur_sum = 0
        for self_time in self.interval.times:
            for other_time in other.times:
                cur_sum += TimeIntervalCollection.distance_from(self_time, other_time)
        return cur_sum

    def earlier_time(self, other):
        """
        Expects another time interval object.
        :param other: The other time interval object to be compared
        :return: The distance from self's time interval to other's time interval
        """
        for self_time in self.interval.times:
            for other_time in other.times:
                if TimeIntervalCollection.earlier_time(self_time, other_time):
                    return True
        return False

    def __str__(self):
        """
        Joins together the data and returns it as a string.
        :return: The string of all the data separated by spaces.
        """
        return ' '.join(str(data) for data in self.data.values())
