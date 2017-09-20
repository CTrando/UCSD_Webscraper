import random
import sqlite3, numpy

from utils import TimeInterval

database = sqlite3.connect('data.db')
database.row_factory = sqlite3.Row
cursor = database.cursor()


class ClassPicker():
    best_candidate = 0
    candidates = []

    def __init__(self, class_set):
        self.class_set = class_set

    def pick_classes(self):
        self._pick_classes(0, [])

    def _pick_classes(self, r, w_set):
        if r >= len(self.class_set):
            self.candidates.append(w_set)
            self.best_candidate = max(self.get_fitness(w_set), self.best_candidate)
            return

        for c in range(0, len(self.class_set[r])):
            c_set = list(w_set)
            if self.class_set[r][c].is_valid(w_set):
                c_set.append(self.class_set[r][c])
                self._pick_classes(r + 1, c_set)

    def get_fitness(self, class_set):
        thing = random.randint(0, 10)
        return thing

    def filter_by_days(self, class_set, str_days):
        ret_list = []
        for row in class_set:
            list = []
            for col in row:
                lec = col.lecture
                if lec.is_in_days(str_days):
                    list.append(col)
            ret_list.append(list)
        return ret_list




class Class:
    def __init__(self, id):
        cursor.execute("SELECT * FROM DATA WHERE ID=?", (id,))
        data = cursor.fetchone()
        if data['LECTURE_KEY']:
            self.lecture = Lecture(data['LECTURE_KEY'])

        if data['LAB_KEY']:
            self.lab = Lab(data['LAB_KEY'])

        if data['DISCUSSION_KEY']:
            self.discussion = Discussion(data['DISCUSSION_KEY'])

        if data['FINAL_KEY']:
            self.final = Final(data['FINAL_KEY'])

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
    def __init__(self, id):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
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
    def __init__(self, id):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
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
    def __init__(self, id):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
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
    def __init__(self, id):
        cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
        data = cursor.fetchone()
        self.course_num = data['COURSE_NUM']
        self.times = data['TIME']
        self.location = data['LOCATION']
        self.room = data['ROOM']
        self.description = data['DESCRIPTION']

    def __str__(self):
        return self.course_num + self.description


my_input = input('Enter the classes that you want like so (CSE 3, CSE 8A, CSE 8B)')
pref_classes = my_input.split(', ')
#pref_classes = ['CSE 3', 'CSE 8A', 'CSE 8B']

class_set = []

for pref_class in pref_classes:
    cursor.execute("SELECT ID FROM DATA WHERE COURSE_NUM = ?", (pref_class,))
    pref_class_set = []
    for id_tuple in cursor.fetchall():
        id = id_tuple['ID']
        class_object = Class(id)
        pref_class_set.append(class_object)
    class_set.append(pref_class_set)

pick = ClassPicker(class_set)
pick.pick_classes()
for candidate in pick.candidates:
    for can in candidate:
        print('[' + str(can), end='] ')
    print()
