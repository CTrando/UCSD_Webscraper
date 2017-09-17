import bs4, os, sqlite3

preset_days = [
    'M', 'Tu', 'W', 'Th', 'F'
]

current_lecture = None


def has_word(buffer, word):
    for sentence in buffer:
        if word in sentence:
            return True
    return False


def made_of_days(section):
    section_len = len(section)
    for day in preset_days:
        if day in section:
            section_len -= len(day)
    return section_len == 0


def get_info(info):
    department = info[0]
    course_num = info[1]
    type = 'TBA'
    location = 'TBA'
    time = 'TBA'
    instructor = 'TBA'
    days = 'TBA'
    if 'FINAL' in info:
        type = 'FINAL'
    elif 'LA' in info:
        type = 'LAB'
    elif 'LE' in info:
        type = 'LECTURE'
        current_lecture = info
    elif 'DI' in info:
        type = 'DISCUSSION'
        instructor = 'N/A'
    elif 'PB' in info:
        type = 'PROBLEM SESSION'

    for i in range(0, len(info)):
        section = info[i]
        if made_of_days(section):
            days = section

        if ':' in section and '(' not in section:
            time = section
            location = info[i + 1]
            i = i + 1
        if ',' in section:
            instructor = section

    description = info[-1]
    return (department, course_num, type, days, time, location, instructor, description)


HTML_STORAGE = 'classes'

dir = os.path.join(os.curdir, HTML_STORAGE, 'CSE')
os.chdir(dir)
buffer_buffer = []
buffer = []
for root, dirs, files in os.walk(os.curdir):
    for file in files:
        with open(file) as html:
            soup = bs4.BeautifulSoup(html, 'lxml')
            for string in soup.stripped_strings:
                if 'CSE' == string:
                    if not has_word(buffer, 'Note') and '|' not in buffer and not has_word(buffer, 'Enrolled') \
                            and not has_word(buffer, 'Section') and not has_word(buffer, 'cancelled'):
                        print(buffer)
                        buffer_buffer.append(get_info(buffer))
                    buffer = []
                buffer.append(string)

os.chdir('C:/Users/ctran/PycharmProjects/UCSD_Webscraper')
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE CLASSES")

cursor.execute("CREATE TABLE CLASSES" +
               "  (ID INTEGER PRIMARY KEY, PARENT_KEY INTEGER, COURSE_DEPARTMENT text, COURSE_NUM real, TYPE text, DAYS text, TIME text, LOCATION text, INSTRUCTOR text, DESCRIPTION text)")

current_row = 0
for thing in buffer_buffer:
    if 'LECTURE' in thing:
        current_row = None
    cursor.execute("INSERT INTO CLASSES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, current_row)+ thing)
    if 'LECTURE' in thing:
        current_row = cursor.lastrowid
# Save (commit) the changes
connection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()
