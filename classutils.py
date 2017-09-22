from timeutils import *


class ClassTemplate:
    def __init__(self, cursor, ID):
        self.cursor = cursor
        self.data = dict(cursor.fetchone())

        self.interval = DefaultTimeInterval()
        self.make_interval()

    def make_interval(self):
        if 'DAYS' in self.data and 'TIME' in self.data:
            interval = TimeInterval(self.data['DAYS'], self.data['TIME'])
            if len(interval.times) > 0:
                self.interval = interval

    def is_in_days(self, str_days):
        return self.data['DAYS'] in str_days

    def overlaps_times_and_days(self, other):
        return self.interval.overlaps_times_and_days(other.interval)

    def overlaps_times(self, other):
        return self.interval.overlaps_times(other)

    def distance_from_interval(self, other):
        return self.interval.distance_from(other)

    def __str__(self):
        return ' '.join(str(data) for data in self.data.values())


class Class(ClassTemplate):
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM DATA WHERE ID=?", (ID,))
        super().__init__(cursor, ID)
        self.lecture = None
        self.lab = None
        self.discussion = None
        self.final = None

        if self.data['LECTURE_KEY']:
            self.lecture = Lecture(cursor, self.data['LECTURE_KEY'])

        if self.data['LAB_KEY']:
            self.lab = Lab(cursor, self.data['LAB_KEY'])

        if self.data['DISCUSSION_KEY']:
            self.discussion = Discussion(cursor, self.data['DISCUSSION_KEY'])

        if self.data['FINAL_KEY']:
            self.final = Final(cursor, self.data['FINAL_KEY'])

        self.subclasses = []
        if self.lab:
            self.subclasses.append(self.lab)
        if self.lecture:
            self.subclasses.append(self.lecture)
        if self.discussion:
            self.subclasses.append(self.discussion)

    def is_valid(self, w_set):
        if len(w_set) == 0:
            return True
        else:
            for choice in w_set:
                if self.overlaps_times_and_days(choice):
                    return False
            return True

    def overlaps_times(self, choice_times):
        flag = False
        if self.lecture and self.lecture.overlaps_times(choice_times):
            flag = True
        if self.discussion and self.discussion.overlaps_times(choice_times):
            flag = True
        if self.lab and self.lab.overlaps_times(choice_times):
            flag = True
        return flag

    def overlaps_times_and_days(self, choice):
        flag = False
        for self_cl in self.subclasses:
            for choice_cl in choice.subclasses:
                if self_cl.overlaps_times_and_days(choice_cl):
                    flag = True
        return flag

    def distance_from_interval(self, other):
        dist = 0
        if self.lecture:
            dist += self.lecture.distance_from_interval(other)
        if self.discussion:
            dist += self.discussion.distance_from_interval(other)
        if self.lab:
            dist += self.lab.distance_from_interval(other)
        return dist

    def __str__(self):
        return str(self.lecture) + ' ' + str(self.discussion) + ' ' + str(self.lab) + ' ' + str(self.final)


class Lecture(ClassTemplate):
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        super().__init__(cursor, ID)


class Lab(ClassTemplate):
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        super().__init__(cursor, ID)


class Discussion(ClassTemplate):
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        super().__init__(cursor, ID)


class Final(ClassTemplate):
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        self.interval = DefaultTimeInterval()
        super().__init__(cursor, ID)
