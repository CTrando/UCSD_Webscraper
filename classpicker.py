import os
import sqlite3
import sys

from classutil.classutils import *
from preferences.time_preference import TimePreference
from settings import DATABASE_PATH, DEFAULT_INTERVAL, HOME_DIR, INTERVALS

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
        # List of possible classes with given course nums
        self.class_set = []
        # List of classes corresponding to correct course nums
        self.pref_classes = []
        # List of possible schedules
        self.candidates = []

        # DP buffer for top down memoization
        self.dp_buffer = {}

        # Preferences
        self.time_pref = TimePreference()

        # Solution variables
        self.best_candidate = None
        self.best_candidate_score = -sys.maxsize

    # Returns a schedule with the given inputs and intervals
    def pick(self, inputs=None, intervals=None):
        # Set INTERVALS to intervals if there are no specified intervals
        if intervals and len(intervals) > 0:
            global INTERVALS
            INTERVALS = intervals

        # Preferred classes received from GUI or command line
        # Formatting inputs
        self.pref_classes = self.format_inputs(inputs)

        # Validating global variables and inputs
        self.validate_variables()
        self.validate_inputs()

        # Get the classes with the specified course names
        self.class_set = self.generate_class_set(self.pref_classes)

        # Getting and validating outputs
        self.get_candidates()
        self.validate_outputs()

        # Return output
        return self.get_output()

    def get_input(self):
        """
        Helper method for grabbing input from the command line.
        """
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
        """
        Ensuring that there is actually an output, otherwise will throw an error.
        """
        if not self.best_candidate:
            raise RuntimeError('It appears that there is no best candidate.')

    def generate_class_set(self, pref_classes):
        """
        Accesses the database and returns the list of classes with the corresponding course num.
        :param pref_classes the list of classes we are trying to select
        :return The corresponding class set
        """

        # Where the classes will be stored
        class_set = []
        # Access each preferred class in given list and store it inside class_set
        for pref_class in pref_classes:
            # Getting the ids of each of the given classes
            self.cursor.execute("SELECT ROWID FROM DATA WHERE COURSE_NUM = ?", (pref_class,))
            # The different sections of the given class
            pref_class_sections = []

            for id_tuple in self.cursor.fetchall():
                id_tuple = dict(id_tuple)
                ID = id_tuple['rowid']
                # Create a class object and add it to the sections
                class_version = Class(self.cursor, ID)
                pref_class_sections.append(class_version)

            # Adding the section to the class set
            class_set.append(pref_class_sections)
        return class_set

    def get_output(self):
        print(self.best_candidate_score)
        print('*' * 10)
        for cl in self.best_candidate:
            print(str(cl))
        print('*' * 10)
        return self.best_candidate

    def get_candidates(self):
        self._get_candidates(0, [])

    def _get_candidates(self, row, w_set):
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

    def get_fitness(self, class_set):
        """
        Get fitness of current class set using top down dynamic programming with memoization
        to store repeating sub-problems. This method will run the get_score method on each of
        the children and return the result. This method only uses one list, although it creates
        many tuples in order to utilize dynamic programming.

        :param class_set: The class set we are observing currently
        :return: The score of the whole class set
        """

        # Base case: when the length of the set is 1, we can run the get_score method
        # and get the score of the only class
        if len(class_set) == 1:
            cl = class_set[0]
            score = .5
            for interval in INTERVALS:
                # Check if hasn't already been calculated yet
                if cl in self.dp_buffer:
                    # Store interval first so can use in keyword
                    score = self.dp_buffer[(interval, cl)]
                    continue

                score += self.get_score(cl, interval)
                self.dp_buffer[(interval, cl)] = score
            return score

        # Otherwise, pop the first class from the set and run the method on the remaining set
        curr_class = class_set.pop()
        # Convert the set into a tuple for dict storage
        working_copy = tuple(class_set)
        score = 0

        # Get the score of the class that we popped
        for interval in INTERVALS:
            score += self.get_score(curr_class, interval)

        # Check if the resulting set is inside the buffer
        # If so, we have already solved the sub-problem and can use its result
        if working_copy in self.dp_buffer:
            # We can add the popped class back to the set and return the value from our dict
            class_set.append(curr_class)
            # No need to store the result here because it is done after the recursive call
            return score + self.dp_buffer[working_copy]

        # Otherwise we can put the score into our DP array so it can be used in the future
        # Recursively go until the base case is run
        cumulative_score = score + self.get_fitness(class_set)
        self.dp_buffer[working_copy] = cumulative_score

        # Add the class back to prevent altering
        class_set.append(curr_class)

        # Return the cumulative score
        return cumulative_score

    def get_score(self, cl, interval):
        """
        Will return the score based on the times and intervals given.

        :param cl: The class we are observing
        :param interval: The specific interval we are comparing to
        :return: the score that we have given this class based on our heuristic
        """
        temp_score = 0
        temp_score += self.time_pref.get_score(cl, interval)

        # TODO fix the heuristic for the score based on time
        return temp_score

        # TODO implement days preferences
