from timeutil.timeutils import *

"""
Puts data into readable format given a table row.
"""


class ClassTemplate:
    def __init__(self, cursor, ID, table='CLASSES'):
        # I don't know why I made the default value CLASSES. Maybe for future code reuse?
        # Maybe to prevent hard coding?

        # Initialize class based on which table
        self.cursor = cursor
        cursor.execute("SELECT * FROM {} WHERE ROWID = ?".format(table), (ID,))

        self.data = dict(cursor.fetchone())

        # Initializing lecture type
        self.type = None
        if 'TYPE' in self.data:
            self.type = self.data['TYPE']

        # Default interval in case it is a final or is formatted strangely
        self.interval = DefaultTimeIntervalCollection()
        self.make_interval()

    """
    The class must not be a final and have a type. Unfortunately that means finals can overlap,
    which can cause problems - will fix later
    """

    def make_interval(self):
        if not self.type:
            return
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
        sum = 0
        for self_time in self.interval.times:
            for other_time in other.times:
                sum += TimeIntervalCollection.distance_from(self_time, other_time)
        return sum

    def __str__(self):
        """
        Joins together the data and returns it as a string.
        :return: The string of all the data separated by spaces.
        """
        return ' '.join(str(data) for data in self.data.values())


"""
Has a dictionary of subclasses. At the moment, new class types must be hardcoded in as follows.
This class is the big superclass controller of all the subclasses.
"""


class Class(ClassTemplate):
    def __init__(self, cursor, ID):
        super().__init__(cursor, ID, table='DATA')
        self.subclasses = {}
        self.final = None

        for subclass_key in self.data:
            if 'KEY' not in subclass_key:
                continue
            subclass = self.data[subclass_key]
            if subclass:
                self.subclasses[subclass_key] = ClassTemplate(cursor, self.data[subclass_key])
                print(subclass)

    """
    Return if the classes overlap. Will add more arguments in the future. 
    """

    def is_valid(self, w_set):
        if len(w_set) == 0:
            return True
        else:
            for choice in w_set:
                # TODO BIG BUG HERE MUST FIX SO FINALS DON'T OVERLAP
                if self.overlaps_times_and_days(choice):
                    return False
            return True

    def overlaps_time(self, choice_time):
        """
        Returns if this class overlaps the time interval.

        :param choice_time the time to be compared
        :return true if the class is partially inside the interval
        """
        # Uses a boolean array
        subclasses = []
        for subclass in self.subclasses.values():
            if subclass.overlaps_time(choice_time):
                subclasses.append(True)
            else:
                subclasses.append(False)
        # Returns if every class overlaps
        return all(subclasses)

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
        subclasses = []
        for subclass in self.subclasses.values():
            if subclass.inside_time(choice_time):
                subclasses.append(True)
            else:
                subclasses.append(False)
        return all(subclasses)

    def distance_from_interval(self, interval):
        """
        Will add up the distances of all subclasses from the intervals.
        :param interval: The interval to be compared to
        :return: The cumulative distance from the interval
        """
        dist = 0
        for subclass in self.subclasses.values():
            dist += subclass.distance_from_interval(interval)
        return max(1, dist)

    def __str__(self):
        """
        To string method for the class
        :return: Returns the to string of all the subclasses combined
        """
        ret = ''
        for cl in self.subclasses.values():
            ret += ' ' + str(cl)
        return ret
