from selenium import webdriver
import os
import sqlite3

from settings import HOME_DIR, DEPARTMENT_URL


class DepartmentScraper:
    def __init__(self):
        os.chdir(os.path.join(HOME_DIR, "driver"))
        self.browser = webdriver.Chrome()
        os.chdir(HOME_DIR)

        from settings import DATABASE_DIR
        self.database = sqlite3.connect(DATABASE_DIR)
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
        departments = self.browser.find_element_by_id('selectedSubjects').find_elements_by_tag_name('option')
        for department in departments:
            department = department.text
            department = department[:4]
            self.cursor.execute('INSERT INTO DEPARTMENT VALUES(?)', (department,))

    def close(self):
        self.database.commit()
        self.database.close()
        self.browser.close()