import os
import sqlite3
import bs4
import time
from settings import HTML_STORAGE, DATABASE_PATH, HOME_DIR


class Parser:
    def __init__(self):
        # initializing database
        os.chdir(HOME_DIR)
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()

        # changing dir for HTML
        self.dir = os.path.join(os.curdir, HTML_STORAGE)
        os.chdir(self.dir)
        self.buffer_buffer = []
        self.buffer = []

    def parse(self):
        print('Beginning parsing.')
        curr_time = time.time()
        self.parse_data()
        self.insert_data()
        self.close()
        fin_time = time.time()
        print('Finished parsing in {} seconds.'.format(fin_time-curr_time))

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
        class_type = row.find(name='td', attrs={'role': 'gridcell',
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

        if None not in (header, section_id, class_type, day, time, location, room, instructor):
            name_desc = header.find_all(name='td')

            name = ' '.join(name_desc[0].text.split())
            section_id = ' '.join(section_id.text.split())
            class_type = ' '.join(class_type.text.split())
            day = ' '.join(day.text.split())
            time = ' '.join(time.text.split())
            location = ' '.join(location.text.split())
            room = ' '.join(room.text.split())
            instructor = ' '.join(instructor.text.split())
            description = ' '.join(name_desc[1].text.split())

            info = [
                name, section_id,
                class_type, day, time,
                location, room, instructor,
                description
            ]
            # passing in a list which will be converted to tuple
            info = self.validate_info(info)
            if info not in self.buffer_buffer:
                self.buffer_buffer.append(info)
                print('*' * 10)
                print(info)

    """
    Method to make final alterations to the dataset. 
    Will put database in cleanable format; however, will not remove
    database. 
    """

    def validate_info(self, data):
        if data[1] == 'FINAL':
            data[1] = None
            data[2] = 'FINAL'
        return tuple(data)

    def insert_data(self):
        self.cursor.execute("DROP TABLE IF EXISTS CLASSES")
        self.cursor.execute("CREATE TABLE CLASSES"
                            "(ID INTEGER PRIMARY KEY, COURSE_NUM REAL, COURSE_ID TEXT, "
                            "TYPE TEXT, DAYS TEXT, TIME TEXT, LOCATION TEXT, ROOM TEXT, "
                            "INSTRUCTOR TEXT, DESCRIPTION TEXT,"
                            "UNIQUE(COURSE_NUM, COURSE_ID, TYPE, DAYS, TIME, LOCATION, ROOM, INSTRUCTOR))")


        self.cursor.execute("BEGIN TRANSACTION")
        for info in self.buffer_buffer:
            self.cursor.execute("INSERT OR IGNORE INTO CLASSES VALUES(?,?,?,?,?,?,?,?, ?, ?)", (None,) + info)

    def close(self):
        self.connection.commit()
        self.connection.close()
