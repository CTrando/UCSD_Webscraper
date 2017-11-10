import os
import sqlite3
import sys

from classutil.classutils import *
from settings import DATABASE_PATH, INTERVALS, DEFAULT_INTERVAL, HOME_DIR

"""
Picks classes and autogenerates schedules.
"""


class ClassPicker():
    def __init__(self):
        # Initializing database
        os.chdir(HOME_DIR)
        self.database = sqlite3.connect(DATABASE_PATH)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()

        # Preparing for DFS
        self.class_set = []
        self.pref_classes = []
        self.candidates = []

        # Solution variables
        self.best_candidate = None
        self.best_candidate_score = -sys.maxsize

    # Returns a schedule with the given inputs and intervals
    def pick(self, inputs=None, intervals=None):
        # Set INTERVALS to intervals
        if intervals and len(intervals) > 0:
            global INTERVALS
            INTERVALS = intervals

        # Formatting inputs
        self.pref_classes = self.format_inputs(inputs)

        # Validating global variables and inputs
        self.validate_variables()
        self.validate_inputs()

        # Starting generation
        self.generate_class_set()

        # Getting and validating outputs
        self.get_candidates()
        self.validate_outputs()

        # Return output
        return self.get_output()

    """
    Command line method for grabbing classes from input.
    """

    def get_input(self):
        my_input = input('Enter the classes that you want like so (CSE 3, CSE 8A, CSE 8B)')
        self.pref_classes = my_input.split(', ')
        self.validate_inputs()

    def format_inputs(self, inputs):
        return [i.upper().rstrip() for i in inputs]

    def validate_variables(self):
        if len(INTERVALS) == 0:
            INTERVALS.append(DEFAULT_INTERVAL)

    def validate_inputs(self):
        for pref_class in self.pref_classes:
            self.cursor.execute("SELECT rowid FROM DATA WHERE COURSE_NUM = ?", (pref_class,))
            if not len(self.cursor.fetchall()) > 0:
                raise IOError('One of the inputs is not a valid class name!')

    def validate_outputs(self):
        if not self.best_candidate:
            raise RuntimeError('It appears that there is no best candidate.')

    """
    Will go into the database and find a list of classes with the given COURSE_NUM and add them 
    to the class set.
    """
    def generate_class_set(self):
        for pref_class in self.pref_classes:
            self.cursor.execute("SELECT rowid FROM DATA WHERE COURSE_NUM = ?", (pref_class,))
            # The different sections of the given class
            pref_class_sections = []

            for id_tuple in self.cursor.fetchall():
                id_tuple = dict(id_tuple)
                ID = id_tuple['rowid']
                # Create a class object and add it to the sections
                class_version = Class(self.cursor, ID)
                pref_class_sections.append(class_version)

            # Adding the section to the class set
            self.class_set.append(pref_class_sections)

    def get_output(self):
        print(self.best_candidate_score)
        print('*' * 10)
        for cl in self.best_candidate:
            print(str(cl))
        print('*' * 10)
        return self.best_candidate

    def get_candidates(self):
        self._get_candidates(0, [])

    """
    The strategy here is to represent the class set as a 2D array, and then have a loop to 
    go down the col. Each time it hits a new col, it will call itself with the next row down.
    
    The algorithm will terminate when the column is greater than the size of the list.
    
    Once the algorithm returns, it will go to its original column and go down one row to 
    call itself again with the next column over. 
    
    If it hits a case where the classes are not valid, then it will backtrack and ignore 
    any combinations with that set of possibilities.   
    
    Visualize as follows:
          COL 0   COL 1
    ROW 0 CSE 11  CSE 11
             |  /\  |   
    ROW 1 CSE 20  CSE 20
    """
    def _get_candidates(self, row, w_set):
        # Make sure column is not greater than size of the array
        # If so, return
        if row >= len(self.class_set):
            # Add itself to the working set
            self.candidates.append(w_set)
            # Update the best_candidate and its score
            if self.get_fitness(w_set) > self.best_candidate_score:
                self.best_candidate_score = self.get_fitness(w_set)
                self.best_candidate = w_set
            return

        # Loop down the column with the length of the amount of classes in a given column
        for col in range(0, len(self.class_set[row])):
            col_set = list(w_set)
            if self.class_set[row][col].is_valid(w_set):
                col_set.append(self.class_set[row][col])
                self._get_candidates(row + 1, col_set)

    """
    Get fitness of the curent class set based on how well it fits into the time preferences.
    """
    def get_fitness(self, class_set):
        score = .5
        for interval in INTERVALS:
            temp_score = .5
            for cl in class_set:
                # If it is contained in the interval reward the set
                if cl.inside_time(interval):
                    temp_score += 1 / cl.distance_from_interval(interval)
                # If it does overlaps in the interval punish the set
                elif cl.overlaps_time(interval):
                    temp_score += .5 * cl.distance_from_interval(interval)
                else:
                    temp_score += .1 * cl.distance_from_interval(interval)
            score = max(temp_score, score)

        return score

    # TODO implement days preferences
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
