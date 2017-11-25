import os
import sqlite3

from timeutil.timeutils import TimeIntervalCollection

"""
This class is a storage area for various variables and settings.
"""

"""
PATHS
"""

# Where the directory is placed
HOME_DIR = os.getcwd()
# Database directory
DATABASE_PATH = os.path.join(HOME_DIR, 'database','data.db')
# Image directory
IMAGE_DIR = os.path.join(HOME_DIR, 'images')

# Where the classes are stored
HTML_STORAGE = os.path.join(HOME_DIR, 'classes')

DRIVER_PATH = os.path.join(HOME_DIR, 'driver', 'chromedriver')

"""
MODES
"""

# Manual mode for logging in
MANUAL_MODE = False

"""
URLS 
"""
# URLs
DEPARTMENT_URL = 'https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm'
WEBREG_URL = 'https://act.ucsd.edu/webreg2/start'

"""
PREFERENCE DATA
"""
# Intervals
INTERVALS = []

# Default interval
DEFAULT_INTERVAL = TimeIntervalCollection(None, '8:00a-12:00p')

"""
VARIABLES
"""
# Current class index for web scraping
CURRENT_CLASS_INDEX = 0


# Time for timeout for browser
TIMEOUT = 30

# Time before class timeout
CLASS_SEARCH_TIMEOUT = 5

# Interval for days on graph
DAY_GRAPH_INTERVAL = .5

POPUP_TEXT_COLOR = (.4, .4, .4, 1)
