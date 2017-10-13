import sqlite3


class ClassHolder:
    def __init__(self):
        self.course_num = None
        self.lab_key = None
        self.lecture_key = None
        self.discussion_key = None
        self.seminar_key = None
        self.final_key = None

    @staticmethod
    def get_type(row):
        for col in row:
            if col in ('LE', 'LA', 'DI', 'SE', 'FINAL'):
                return col
        return None

    @staticmethod
    def is_canceled(row):
        if 'cancelled' in row:
            return True
        return False

    @staticmethod
    def is_review_session(row):
        if 'Review Sessions' in row:
            return True
        return False

    @classmethod
    def insert_lecture(self, cursor, course_num, lecture_key):
        cursor.execute('SELECT COUNT(1) FROM DATA WHERE COURSE_NUM = ? AND LECTURE_KEY IS NULL', (course_num,))
        num = cursor.fetchone()
        if num[0] > 0:
            cursor.execute('UPDATE DATA SET LECTURE_KEY = ? WHERE COURSE_NUM = ? AND LECTURE_KEY IS NULL',
                           (lecture_key, course_num))
        else:
            cursor.execute('INSERT INTO DATA VALUES(?,?,?,?,?,?,?)',
                           (None, course_num, lecture_key, None, None, None, None))

    @staticmethod
    def insert_discussion(cursor, course_num, discussion_key):
        cursor.execute('SELECT COUNT(1) FROM DATA WHERE COURSE_NUM = ? AND DISCUSSION_KEY IS NULL', (course_num,))
        num = cursor.fetchone()
        if num[0] > 0:
            cursor.execute('UPDATE DATA SET DISCUSSION_KEY = ? WHERE COURSE_NUM = ? AND DISCUSSION_KEY IS NULL',
                           (discussion_key, course_num))
        else:
            cursor.execute('INSERT INTO DATA VALUES(?,?,?,?,?,?,?)',
                           (None, course_num, None, None, discussion_key, None, None))

    @staticmethod
    def insert_lab(cursor, course_num, lab_key):
        cursor.execute('SELECT COUNT(1) FROM DATA WHERE COURSE_NUM = ? AND LAB_KEY IS NULL', (course_num,))
        num = cursor.fetchone()
        if num[0] > 0:
            cursor.execute('UPDATE DATA SET LAB_KEY = ? WHERE COURSE_NUM = ? AND LAB_KEY IS NULL',
                           (lab_key, course_num))
        else:
            cursor.execute('INSERT INTO DATA VALUES(?,?,?,?,?,?,?)',
                           (None, course_num, None, lab_key, None, None, None))

    @staticmethod
    def insert_seminar(cursor, course_num, seminar_key):
        cursor.execute('SELECT COUNT(1) FROM DATA WHERE COURSE_NUM = ? AND SEMINAR_KEY IS NULL', (seminar_key,))
        num = cursor.fetchone()
        if num[0] > 0:
            cursor.execute('UPDATE DATA SET SEMINAR_KEY = ? WHERE COURSE_NUM = ? AND SEMINAR_KEY IS NULL',
                           (seminar_key, course_num))
        else:
            cursor.execute('INSERT INTO DATA VALUES(?,?,?,?,?,?,?)',
                           (None, course_num, None, None, None, seminar_key, None))

    @staticmethod
    def insert_final(cursor, course_num, final_key):
        cursor.execute('SELECT COUNT(1) FROM DATA WHERE COURSE_NUM = ?', (course_num,))
        num = cursor.fetchone()
        if num[0] > 0:
            cursor.execute('UPDATE DATA SET FINAL_KEY = ? WHERE COURSE_NUM = ? AND FINAL_KEY IS NULL',
                           (final_key, course_num))
        else:
            cursor.execute('INSERT INTO DATA VALUES(?,?,?,?,?,?,?)',
                           (None, course_num, None, None, None, None, final_key))


class Cleaner:
    def __init__(self):
        self.database = sqlite3.connect('data/data.db')
        self.cursor = self.database.cursor()

    def clean(self):
        self.begin()
        self.create_links()
        self.close()

    def begin(self):
        self.cursor.execute('DROP TABLE IF EXISTS DATA')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS DATA '
            '(ID INTEGER PRIMARY KEY, COURSE_NUM TEXT, '
            'LECTURE_KEY INTEGER, LAB_KEY INTEGER, '
            'DISCUSSION_KEY INTEGER, SEMINAR_KEY INTEGER, FINAL_KEY INTEGER)'
        )

    def create_links(self):
        self.cursor.execute("SELECT DISTINCT COURSE_NUM FROM CLASSES")
        class_list = self.cursor.fetchall()
        for course_num in class_list:
            self.cursor.execute("SELECT ID, COURSE_ID, DAYS, TYPE "
                                "FROM CLASSES WHERE COURSE_NUM = ?"
                                "ORDER BY ID", course_num)

            '''
                The strategy here is to loop through each class data set (Every class that has the same 
                course num), and then if it is a lecture, create a new row inside the database with the
                lab, discussion, and final keys not filled up 
                
                As we continue to loop through the set of data, we will encounter the corresponding
                extra classes (the matching discussion section and such), and we will go to our table, 
                find all the classes with the same course num that don't have any values for the section,
                and populate it with the correct key.
                
                This is how we deal with discussions, labs, and finals sometimes matching to multiple lectures.
            '''

            for class_info in self.cursor.fetchall():
                print(class_info)
                print(course_num)
                if ClassHolder.is_canceled(class_info) or ClassHolder.is_review_session(class_info):
                    continue
                if ClassHolder.get_type(class_info) == 'LE':
                    ClassHolder.insert_lecture(self.cursor, course_num[0], class_info[0])
                elif ClassHolder.get_type(class_info) == 'DI':
                    ClassHolder.insert_discussion(self.cursor, course_num[0], class_info[0])
                elif ClassHolder.get_type(class_info) == 'FINAL':
                    ClassHolder.insert_final(self.cursor, course_num[0], class_info[0])
                elif ClassHolder.get_type(class_info) == 'LA':
                    ClassHolder.insert_lab(self.cursor, course_num[0], class_info[0])
                elif ClassHolder.get_type(class_info) == 'SE':
                    ClassHolder.insert_seminar(self.cursor, course_num[0], class_info[0])
                self.database.commit()
            print('*' * 10)

    def close(self):
        self.database.commit()
        self.database.close()
