from selenium import webdriver
import os
import sqlite3

from settings import HOME_DIR
from settings import DEPARTMENT_URL
from settings import DATABASE_PATH


class DepartmentScraper:
    INFO_MAX_INDEX = 4

    def __init__(self):
        # Start up the browser
        os.chdir(os.path.join(HOME_DIR, "driver"))
        self.browser = webdriver.Chrome()

        # Go back to home directory
        os.chdir(HOME_DIR)

        # Establish database connection
        self.database = sqlite3.connect(DATABASE_PATH)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()

    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS DEPARTMENT')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS DEPARTMENT (DEPT_CODE TEXT)')

    def scrape(self):
        self.create_table()
        self.search()
        self.get_departments()
        self.close()

    def search(self):
        self.browser.get(DEPARTMENT_URL)

    def get_departments(self):
        departments = self.browser.find_element_by_id('selectedSubjects') \
            .find_elements_by_tag_name('option')
        for department in departments:
            department = department.text
            # Get first four elements
            department = department[:DepartmentScraper.INFO_MAX_INDEX]
            # Making sure department is in the correct format
            department = self.normalize_department(department)
            self.cursor.execute('INSERT INTO DEPARTMENT VALUES(?)', (department,))

    def normalize_department(self, department):
        return department.strip()

    def close(self):
        self.database.commit()
        self.database.close()
        self.browser.close()
