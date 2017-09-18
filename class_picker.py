import random
import sqlite3, numpy

database = sqlite3.connect('real_data.db')
database.row_factory = sqlite3.Row
cursor = database.cursor()

class_database = sqlite3.connect('data.db')
class_database.row_factory = sqlite3.Row
class_cursor = class_database.cursor()


class ClassPicker():
    best_candidate = 0

    def __init__(self, class_set):
        self.class_set = class_set

    def pick_classes(self):
        self._pick_classes(0, [])

    def _pick_classes(self, r, w_set):
        if r >= len(self.class_set):
            self.best_candidate = max(self.get_fitness(w_set), self.best_candidate)
            return

        for c in range(0, len(self.class_set[r])):
            c_set = list(w_set)
            if self.class_set[r][c].is_valid(w_set):
                c_set.append(self.class_set[r][c])
                self._pick_classes(r + 1, c_set)

    def get_fitness(self, class_set):
        thing = random.randint(0,10)
        return thing



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
        return False

    def __str__(self):
        return str(self.lecture)


class Lecture:
    def __init__(self, id):
        class_cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
        data = class_cursor.fetchone()
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
        return self.course_num + self.course_id + self.type + self.days + self.instructor + self.description


class Lab:
    def __init__(self, id):
        class_cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
        data = class_cursor.fetchone()
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
        class_cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
        data = class_cursor.fetchone()
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
        class_cursor.execute("SELECT * FROM CLASSES WHERE ID = ?", (id,))
        data = class_cursor.fetchone()
        self.course_num = data['COURSE_NUM']
        self.times = data['TIME']
        self.location = data['LOCATION']
        self.room = data['ROOM']
        self.description = data['DESCRIPTION']

    def __str__(self):
        return self.course_num + self.description


input = input('Enter the classes that you want like so (CSE 3, CSE 8A, CSE 8B)')
# pref_classes = input.split(', ')
pref_classes = ['CSE 3', 'CSE 8A', 'CSE 8B']

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
print(pick.best_candidate)