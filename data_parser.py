import bs4
import os
import sqlite3
from settings import DEPARTMENTS, HTML_STORAGE


class Parser:
    def __init__(self):
        self.dir = os.path.join(os.curdir, HTML_STORAGE)
        os.chdir(self.dir)
        self.buffer_buffer = []
        self.buffer = []

    def parse(self):
        self.parse_data()
        self.insert_data()

    def parse_data(self):
        for root, dirs, files in os.walk(os.curdir):
            for dir in dirs:
                for file in os.listdir(dir):
                    with open(os.path.join(dir, file)) as html:
                        soup = bs4.BeautifulSoup(html, 'lxml')
                        rows = soup.find_all(name='tr')
                        for row in rows:
                            self.parse_row(row)

    def parse_row(self, row):
        header = row.find(name='table', attrs={'id': 'search-group-header-id'})
        section_id = row.find(name='td', attrs={'role': 'gridcell',
                                                'aria-describedby': 'search-div-b-table_SECTION_NUMBER'})
        lecture_type = row.find(name='td', attrs={'role': 'gridcell',
                                                  'aria-describedby': 'search-div-b-table_FK_CDI_INSTR_TYPE'})
        day = row.find(name='td',
                       attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_DAY_CODE'})
        time = row.find(name='td',
                        attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_coltime'})
        location = row.find(name='td',
                            attrs={'role': 'gridcell',
                                   'aria-describedby': 'search-div-b-table_BLDG_CODE'})
        room = row.find(name='td',
                        attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_ROOM_CODE'})
        instructor = row.find(name='td', attrs={'role': 'gridcell',
                                                'aria-describedby': 'search-div-b-table_PERSON_FULL_NAME'})

        if None not in (header, section_id, lecture_type, day, time, location, room, instructor):
            name_desc = header.find_all(name='td')

            name = ' '.join(name_desc[0].text.split())
            section_id = ' '.join(section_id.text.split())
            lecture_type = ' '.join(lecture_type.text.split())
            day = ' '.join(day.text.split())
            time = ' '.join(time.text.split())
            location = ' '.join(location.text.split())
            room = ' '.join(room.text.split())
            instructor = ' '.join(instructor.text.split())
            description = ' '.join(name_desc[1].text.split())

            info = (
                name, section_id,
                lecture_type, day, time,
                location, room, instructor,
                description
            )
            self.buffer_buffer.append(info)
            print('*' * 10)
            print(info)

    def insert_data(self):
        os.chdir('C:/Users/ctran/PycharmProjects/UCSD_Webscraper')
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS CLASSES"
                       "(ID INTEGER PRIMARY KEY, COURSE_NUM REAL, COURSE_ID TEXT, "
                       "TYPE TEXT, DAYS TEXT, TIME TEXT, LOCATION TEXT, ROOM TEXT, "
                       "INSTRUCTOR TEXT, DESCRIPTION TEXT,"

                       "UNIQUE(COURSE_NUM, COURSE_ID, TYPE, DAYS, TIME, "
                       "LOCATION, ROOM, INSTRUCTOR, DESCRIPTION))")

        for info in self.buffer_buffer:
            cursor.execute("INSERT OR IGNORE INTO CLASSES VALUES(?,?,?,?,?,?,?,?, ?, ?)", (None,) + info)
        connection.commit()
        connection.close()
