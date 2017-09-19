import bs4, os, sqlite3
from settings import DEPARTMENT

HTML_STORAGE = 'classes'

dir = os.path.join(os.curdir, HTML_STORAGE, DEPARTMENT)
os.chdir(dir)
buffer_buffer = []
buffer = []
for root, dirs, files in os.walk(os.curdir):
    for file in files:
        with open(file) as html:
            soup = bs4.BeautifulSoup(html, 'lxml')
            rows = soup.find_all(name='tr')
            for row in rows:
                header = row.find(name='table', attrs={'id': 'search-group-header-id'})
                section_id = row.find(name='td', attrs={'role': 'gridcell',
                                                        'aria-describedby': 'search-div-b-table_SECTION_NUMBER'})
                lecture_type = row.find(name='td', attrs={'role': 'gridcell',
                                                          'aria-describedby': 'search-div-b-table_FK_CDI_INSTR_TYPE'})
                day = row.find(name='td', attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_DAY_CODE'})
                time = row.find(name='td', attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_coltime'})
                location = row.find(name='td',
                                    attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_BLDG_CODE'})
                room = row.find(name='td',
                                attrs={'role': 'gridcell', 'aria-describedby': 'search-div-b-table_ROOM_CODE'})
                instructor = row.find(name='td', attrs={'role': 'gridcell',
                                                        'aria-describedby': 'search-div-b-table_PERSON_FULL_NAME'})

                if not None in (header, section_id, lecture_type, day, time, location, room, instructor):
                    name_desc = header.find_all(name='td')

                    course_department = 'CSE'
                    name = ' '.join(name_desc[0].text.split())
                    section_id = ' '.join(section_id.text.split())
                    lecture_type = ' '.join(lecture_type.text.split())
                    day = ' '.join(day.text.split())
                    time = ' '.join(time.text.split())
                    location = ' '.join(location.text.split())
                    room = ' '.join(room.text.split())
                    instructor = ' '.join(instructor.text.split())
                    description = ' '.join(name_desc[1].text.split())

                    print(name, description, section_id, lecture_type, day, time, location, room, instructor)

                    print('*' * 10)
                    vals = (None, name, section_id, lecture_type, day, time, location, room, instructor, description)
                    buffer_buffer.append(vals)

os.chdir('C:/Users/ctran/PycharmProjects/UCSD_Webscraper')
connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS CLASSES" +
               "  (ID INTEGER PRIMARY KEY, COURSE_NUM real, COURSE_ID text, TYPE text, DAYS text, TIME text, LOCATION text, ROOM text, INSTRUCTOR text, DESCRIPTION text," +
               "UNIQUE(COURSE_NUM, COURSE_ID, TYPE, DAYS, TIME, LOCATION, ROOM, INSTRUCTOR, DESCRIPTION))")

for vals in buffer_buffer:
    cursor.execute("INSERT OR IGNORE INTO CLASSES VALUES(?,?,?,?,?,?,?,?, ?, ?)", vals)
connection.commit()
connection.close()
