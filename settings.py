import sqlite3

import departmentscraper
from timeutils import TimeInterval

database = sqlite3.connect('data.db')
cursor = database.cursor()
cursor.execute('SELECT DEPT_CODE FROM DEPARTMENT')
DEPARTMENTS = []
depts = cursor.fetchall()
if len(depts) <= 0:
    dept_scraper = departmentscraper.DepartmentScraper()
    dept_scraper.scrape()
    cursor.execute('SELECT DEPT_CODE FROM DEPARTMENT')
    depts = cursor.fetchall()

for code in depts:
    DEPARTMENTS.append(code[0].strip())

HTML_STORAGE = 'classes'
INTERVALS = [TimeInterval(None, '8:00a-12:00p'), TimeInterval(None, '7:00p-10:00p')]
