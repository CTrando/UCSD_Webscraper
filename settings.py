import os
import sqlite3

from timeutil.timeutils import TimeInterval

# Where the directory is placed
HOME_DIR = os.getcwd()
# Database directory
DATABASE_PATH = 'database/data.db'
# Image directory
IMAGE_DIR = 'images'

# URLs
DEPARTMENT_URL = 'https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm'
WEBREG_URL = 'https://act.ucsd.edu/webreg2/start'

# Is list of current departments
DEPARTMENTS = []

# Connect to the department database and see if it has names
database = sqlite3.connect(DATABASE_PATH)
cursor = database.cursor()
cursor.execute('SELECT DEPT_CODE FROM DEPARTMENT')
depts = cursor.fetchall()

# If no departments in database, then scrape
if len(depts) <= 0:
    from scraper import departmentscraper

    dept_scraper = departmentscraper.DepartmentScraper()
    dept_scraper.scrape()
    # Update depts
    cursor.execute('SELECT DEPT_CODE FROM DEPARTMENT')
    depts = cursor.fetchall()

# Put depts into DEPARTMENTS, making sure to normalize string
for code in depts:
    DEPARTMENTS.append(code[0].strip())

# Where the classes are stored
HTML_STORAGE = 'classes'

# Intervals
INTERVALS = []

# Default interval
DEFAULT_INTERVAL = TimeInterval(None, '8:00a-12:00p')
