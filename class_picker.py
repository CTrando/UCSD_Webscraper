import random
import sqlite3
from utils import *

class ClassPicker():
    def __init__(self):
        self.database = sqlite3.connect('data.db')
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()

        self.class_set = []
        self.pref_classes = []
        self.candidates = []
        self.best_candidate = 0

    def pick(self):
        self.get_input()
        self.generate_class_set()
        self.get_candidates()
        self.get_output()

    def get_input(self):
        my_input = input('Enter the classes that you want like so (CSE 3, CSE 8A, CSE 8B)')
        self.pref_classes = my_input.split(', ')

    def generate_class_set(self):
        for pref_class in self.pref_classes:
            self.cursor.execute("SELECT ID FROM DATA WHERE COURSE_NUM = ?", (pref_class,))
            pref_class_versions = []

            for id_tuple in self.cursor.fetchall():
                ID = id_tuple['ID']
                class_version = Class(self.cursor, ID)
                pref_class_versions.append(class_version)

            self.class_set.append(pref_class_versions)

    def get_output(self):
        for candidate_list in self.candidates:
            for candidate in candidate_list:
                print('[' + str(candidate) + ']')
            print('*'*10)

    def get_candidates(self):
        self._get_candidates(0, [])

    def _get_candidates(self, r, w_set):
        if r >= len(self.class_set):
            self.candidates.append(w_set)
            self.best_candidate = max(self.get_fitness(w_set), self.best_candidate)
            return

        for c in range(0, len(self.class_set[r])):
            c_set = list(w_set)
            if self.class_set[r][c].is_valid(w_set):
                c_set.append(self.class_set[r][c])
                self._get_candidates(r + 1, c_set)

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
