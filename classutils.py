from timeutils import *


class ClassTemplate:
    def __init__(self, cursor, ID, table='CLASSES'):
        self.cursor = cursor
        cursor.execute("SELECT * FROM {} WHERE ID = ?".format(table), (ID,))

        self.data = dict(cursor.fetchone())
        self.type = None
        if 'TYPE' in self.data:
            self.type = self.data['TYPE']

        self.interval = DefaultTimeInterval()
        self.make_interval()

    def make_interval(self):
        if not self.type:
            return
        if self.type == 'FINAL':
            return
        if 'DAYS' in self.data and 'TIME' in self.data:
            interval = TimeInterval(self.data['DAYS'], self.data['TIME'])
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

    def is_valid(self, w_set):
        if len(w_set) == 0:
            return True
        else:
            for choice in w_set:
                #TODO BIG BUG HERE MUST FIX SO FINALS DONT OVERLAP
                if self.overlaps_times_and_days(choice):
                    return False
            return True

    def overlaps_time(self, choice_time):
        subclasses = []
        for subclass in self.subclasses.values():
            if subclass.overlaps_time(choice_time):
                subclasses.append(True)
            else:
                subclasses.append(False)
        return all(subclasses)

    def overlaps_times_and_days(self, choice):
        for self_cl in self.subclasses.values():
            for choice_cl in choice.subclasses.values():
                if self_cl.overlaps_times_and_days(choice_cl):
                    return True
        return False

    def inside_time(self, choice_time):
        subclasses = []
        for subclass in self.subclasses.values():
            if subclass.inside_time(choice_time):
                subclasses.append(True)
            else:
                subclasses.append(False)
        return all(subclasses)

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
