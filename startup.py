"""
This class is responsible for ensuring the proper state upon startup.
"""

import sqlite3

from settings import DATABASE_PATH

database = sqlite3.connect(DATABASE_PATH)
cursor = database.cursor()


# TODO flesh out this method with other startup needs
def start():
    # Creating the department table
    cursor.execute('CREATE TABLE IF NOT EXISTS DEPARTMENT (DEPT_CODE TEXT)')
