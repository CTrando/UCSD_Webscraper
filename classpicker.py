import sqlite3
import sys

import os

from classutils import *
from settings import INTERVALS


class ClassPicker():
    def __init__(self):
        # initializing database
        os.chdir('C:/Users/ctran/PycharmProjects/UCSD_Webscraper')
        self.database = sqlite3.connect('data/data.db')
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()

        self.class_set = []
        self.pref_classes = []
        self.candidates = []
        self.best_candidate = None
        self.best_candidate_score = -sys.maxsize

    def pick(self, inputs=None, intervals=None):
        if intervals and len(intervals) > 0:
            global INTERVALS
            INTERVALS = intervals
        # if not inputs:
        #     self.get_input()
        # else:
        self.pref_classes = [i.upper() for i in inputs]
        self.validate_inputs()
        self.generate_class_set()
        self.get_candidates()
        self.validate_outputs()
        return self.get_output()

    def get_input(self):
        my_input = input('Enter the classes that you want like so (CSE 3, CSE 8A, CSE 8B)')
        self.pref_classes = my_input.split(', ')
        self.validate_inputs()

    def validate_inputs(self):
        for pref_class in self.pref_classes:
            self.cursor.execute("SELECT ID FROM DATA WHERE COURSE_NUM = ?", (pref_class,))
            if not len(self.cursor.fetchall()) > 0:
                raise IOError('One of the inputs is not a valid class name!')

    def validate_outputs(self):
        if not self.best_candidate:
            raise ValueError('It appears that there is no best candidate.')

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
        print(self.best_candidate_score)
        print('*' * 10)
        for cl in self.best_candidate:
            print(str(cl))
        print('*' * 10)
        return self.best_candidate

    def get_string_output(self):
        return [str(cl) for cl in self.best_candidate]

    def get_candidates(self):
        self._get_candidates(0, [])

    def _get_candidates(self, r, w_set):
        if r >= len(self.class_set):
            self.candidates.append(w_set)
            if self.get_fitness(w_set) > self.best_candidate_score:
                self.best_candidate_score = self.get_fitness(w_set)
                self.best_candidate = w_set
            return

        for c in range(0, len(self.class_set[r])):
            c_set = list(w_set)
            if self.class_set[r][c].is_valid(w_set):
                c_set.append(self.class_set[r][c])
                self._get_candidates(r + 1, c_set)

    def get_fitness(self, class_set):
        score = .5
        for interval in INTERVALS:
            temp_score = .5
            for cl in class_set:
                if cl.inside_time(interval):
                    temp_score += 1 / cl.distance_from_interval(interval)
                if not cl.overlaps_time(interval):
                    temp_score -= .1 * cl.distance_from_interval(interval)
            score = max(temp_score, score)

        return score

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
