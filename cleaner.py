import sqlite3

real_data = sqlite3.connect('real_data.db')
r_cursor = real_data.cursor()
r_cursor.execute('DROP TABLE DATA')
r_cursor.execute(
    'CREATE TABLE IF NOT EXISTS DATA (ID INTEGER PRIMARY KEY, COURSE_NUM TEXT, LECTURE_KEY INTEGER, LAB_KEY INTEGER, DISCUSSION_KEY INTEGER, FINAL_KEY INTEGER)')


class ClassHolder:
    def __init__(self):
        self.course_num = None
        self.lab_key = None
        self.lecture_key = None
        self.discussion_key = None
        self.final_key = None

    @staticmethod
    def get_type(row):
        for col in row:
            if col in ('LE', 'LA', 'DI', 'FINAL'):
                return col
        return None

    @staticmethod
    def insert_discussion(course_num, discussion_id):
        r_cursor.execute("UPDATE DATA SET DISCUSSION_KEY = ? WHERE COURSE_NUM = ? AND DISCUSSION_KEY IS NULL",
                         (discussion_id, course_num))

    @staticmethod
    def insert_lab(course_num, lab_id):
        r_cursor.execute("UPDATE DATA SET LAB_KEY = ? WHERE COURSE_NUM = ? AND LAB_KEY IS NULL", (lab_id, course_num))

    @staticmethod
    def insert_final(course_num, final_id):
        r_cursor.execute("UPDATE DATA SET FINAL_KEY = ? WHERE COURSE_NUM = ? AND FINAL_KEY IS NULL",
                         (final_id, course_num))

    def save(self):
        r_cursor.execute("INSERT INTO DATA VALUES(?,?,?,?,?,?)",
                         (None, self.course_num, self.lecture_key, self.lab_key, self.discussion_key, self.final_key))


database = sqlite3.connect('data.db')
cursor = database.cursor()
cursor.execute("SELECT DISTINCT COURSE_NUM FROM CLASSES")
for num in cursor.fetchall():
    cursor.execute("SELECT ID, COURSE_ID, TYPE FROM CLASSES WHERE COURSE_NUM = ?", num)
    for thing in cursor.fetchall():
        print(thing)
        if ClassHolder.get_type(thing) == 'LE':
            new_class = ClassHolder()
            new_class.course_num = num[0]
            new_class.lecture_key = thing[0]
            new_class.save()
        elif ClassHolder.get_type(thing) == 'DI':
            ClassHolder.insert_discussion(num[0], thing[0])
        elif ClassHolder.get_type(thing) == 'FINAL':
            ClassHolder.insert_final(num[0], thing[0])
        elif ClassHolder.get_type(thing) == 'LA':
            ClassHolder.insert_lab(num[0], thing[0])
    print('*' * 10)

real_data.commit()
real_data.close()
