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
        cursor.execute("SELECT * FROM {} WHERE ID = ?".format(table), (ID,))

        self.data = dict(cursor.fetchone())

        # Initializing lecture type
        self.type = None
        if 'TYPE' in self.data:
            self.type = self.data['TYPE']

        # Default interval in case it is a final or is formatted strangely
        self.interval = DefaultTimeInterval()
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
            interval = TimeInterval(self.data['DAYS'], self.data['TIME'])
            # Make sure that the interval has valid times
            if len(interval.times) > 0:
                self.interval = interval

    def is_in_days(self, str_days):
        return self.data['DAYS'] in str_days

    def overlaps_times_and_days(self, other):
        return self.interval.overlaps_times_and_days(other.interval)

    def inside_time(self, other):
        return self.interval.inside_time(other)

    def overlaps_time(self, other):
        return self.interval.overlaps_time(other)

    def distance_from_interval(self, other):
        return self.interval.distance_from(other)

    def __str__(self):
        return ' '.join(str(data) for data in self.data.values())


"""
Has a dictionary of subclasses. At the moment, new class types must be hardcoded in as follows.
This class is the big superclass controller of all the subclasses.
"""


class Class(ClassTemplate):
    def __init__(self, cursor, ID):
        super().__init__(cursor, ID, table='DATA')
        self.subclasses = {}

        if self.data['LECTURE_KEY']:
            self.subclasses['LE'] = ClassTemplate(cursor, self.data['LECTURE_KEY'])

        if self.data['LAB_KEY']:
            self.subclasses['LA'] = ClassTemplate(cursor, self.data['LAB_KEY'])

        if self.data['DISCUSSION_KEY']:
            self.subclasses['DI'] = ClassTemplate(cursor, self.data['DISCUSSION_KEY'])

        if self.data['FINAL_KEY']:
            self.subclasses['FINAL'] = ClassTemplate(cursor, self.data['FINAL_KEY'])

        if self.data['SEMINAR_KEY']:
            self.subclasses['SE'] = ClassTemplate(cursor, self.data['SEMINAR_KEY'])

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

    """
    Returns if this class overlaps the time interval.
    """
    def overlaps_time(self, choice_time):
        # Uses a boolean array
        subclasses = []
        for subclass in self.subclasses.values():
            if subclass.overlaps_time(choice_time):
                subclasses.append(True)
            else:
                subclasses.append(False)
        # Returns if every class overlaps
        return all(subclasses)

    """
    Returns if the class overlaps times and days with another class.
    """
    def overlaps_times_and_days(self, choice):
        for self_cl in self.subclasses.values():
            for choice_cl in choice.subclasses.values():
                if self_cl.overlaps_times_and_days(choice_cl):
                    return True
        return False

    """
    Check if class is inside a time interval, not necessarily contained in it.
    """
    def inside_time(self, choice_time):
        subclasses = []
        for subclass in self.subclasses.values():
            if subclass.inside_time(choice_time):
                subclasses.append(True)
            else:
                subclasses.append(False)
        return all(subclasses)

    """
    Computes the distance from the class's times to the given time interval.
    This method is very likely broken. 
    """
    def distance_from_interval(self, interval):
        dist = 0
        for subclass in self.subclasses.values():
            if not subclass.inside_time(interval):
                dist += subclass.distance_from_interval(interval)
        return max(1, dist)

    def __str__(self):
        ret = ''
        for cl in self.subclasses.values():
            ret += ' ' + str(cl)
        return ret
