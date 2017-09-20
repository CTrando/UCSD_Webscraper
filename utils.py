import datetime, time

PRESET_DAYS = ['M', 'Tu', 'W', 'Th', 'F']


class TimeInterval:
    """
    Expects day_col formatted as combinations of PRESET_DAYS
    Expects time_col formatted as TIME + a/p + : + TIME + a/p
    """
    def __init__(self, day_col, time_col):
        self.sanitize_inputs(day_col, time_col)

    def sanitize_inputs(self, day_col, time_col):
        self.days = self.get_days(day_col)
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
            g_time = time.strptime(b_time, '%I:%M%p')
            ret_times.append(g_time)
        return ret_times

    def overlaps(self, other):
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


class Class:
    def __init__(self, cursor, ID):
        self.cursor = cursor
        self.cursor.execute("SELECT * FROM DATA WHERE ID=?", (ID,))
        data = cursor.fetchone()
        if data['LECTURE_KEY']:
            self.lecture = Lecture(cursor, data['LECTURE_KEY'])

        if data['LAB_KEY']:
            self.lab = Lab(cursor, data['LAB_KEY'])

        if data['DISCUSSION_KEY']:
            self.discussion = Discussion(cursor, data['DISCUSSION_KEY'])

        if data['FINAL_KEY']:
            self.final = Final(cursor, data['FINAL_KEY'])

    def is_valid(self, w_set):
        if len(w_set) == 0:
            return True
        else:
            for choice in w_set:
                if self.overlaps(choice):
                    return False
            return True

    def overlaps(self, choice):
        my_lecture_interval = TimeInterval(self.lecture.days, self.lecture.times)
        choice_interval = TimeInterval(choice.lecture.days, choice.lecture.times)
        return my_lecture_interval.overlaps(choice_interval)

    def __str__(self):
        return str(self.lecture)


class Lecture:
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        data = cursor.fetchone()
        self.course_num = data['COURSE_NUM']
        self.course_id = data['COURSE_ID']
        self.type = data['TYPE']
        self.days = data['DAYS']
        self.times = data['TIME']
        self.location = data['LOCATION']
        self.room = data['ROOM']
        self.instructor = data['INSTRUCTOR']
        self.description = data['DESCRIPTION']

    def __str__(self):
        list = self.course_num, self.course_id, self.type, self.times, self.days, self.instructor, self.description
        return ' '.join(list)

    def is_in_days(self, str_days):
        return self.days in str_days


class Lab:
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        data = cursor.fetchone()
        self.course_num = data['COURSE_NUM']
        self.type = data['TYPE']
        self.days = data['DAYS']
        self.times = data['TIME']
        self.location = data['LOCATION']
        self.room = data['ROOM']
        self.description = data['DESCRIPTION']

    def __str__(self):
        return self.course_num + self.type + self.days + self.description


class Discussion:
    def __init__(self, cursor, ID):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (ID,))
        data = cursor.fetchone()
        self.course_num = data['COURSE_NUM']
        self.type = data['TYPE']
        self.days = data['DAYS']
        self.times = data['TIME']
        self.location = data['LOCATION']
        self.room = data['ROOM']
        self.description = data['DESCRIPTION']

    def __str__(self):
        return self.course_num + self.type + self.days + self.description


class Final:
    def __init__(self, cursor, ID):
        cursor.execute('SELECT * FROM CLASSES WHERE ID = ?', (ID,))
        data = cursor.fetchone()
        self.course_num = data['COURSE_NUM']
        self.times = data['TIME']
        self.location = data['LOCATION']
        self.room = data['ROOM']
        self.description = data['DESCRIPTION']

    def __str__(self):
        return self.course_num + self.description
