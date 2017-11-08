import sqlite3
import time

from settings import DATABASE_PATH

"""
Convenience class for holding the keys to the CLASSES table representing
the subclasses in this specific class.
"""


class ClassHolder:
    def __init__(self):
        """
        There is a class key for each type of class. That would be lectures, discussions,
        finals, etc. At the moment, we have to add a new key if we want to make
        adjustments to a new type.
        """
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

    """
    Returns if the class is cancelled.
    """

    @staticmethod
    def is_canceled(row):
        if 'cancelled' in row:
            return True
        return False

    """
    Returns if the class is a review session.
    """

    @staticmethod
    def is_review_session(row):
        if 'Review Sessions' in row:
            return True
        return False

    """
    The general strategy for the following methods is to look at the table and see if there are
    any column with the same COURSE_NUM but a null corresponding key.
         
    That means that for insert lecture, the code will look at the database for any rows with 
    the same COURSE_NUM but no lecture key. 
    
    Because of how the data is funneled in, there should be no cases where a lecture key corresponds
    to the right class but the wrong class section (Could still happen).
    
    If there is no corresponding COURSE_NUM row, then it will create a row.
    The only exception is the final, where an extra final is not enough to make a class by itself. 
    """

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

    """
    Important! This method is slightly different
    """

    @staticmethod
    def insert_final(cursor, course_num, final_key):
        # Difference is in the line below with not testing if the FINAL_KEY is null
        cursor.execute('SELECT COUNT(1) FROM DATA WHERE COURSE_NUM = ?', (course_num,))
        num = cursor.fetchone()
        if num[0] > 0:
            cursor.execute('UPDATE DATA SET FINAL_KEY = ? WHERE COURSE_NUM = ? AND FINAL_KEY IS NULL',
                           (final_key, course_num))
        else:
            cursor.execute('INSERT INTO DATA VALUES(?,?,?,?,?,?,?)',
                           (None, course_num, None, None, None, None, final_key))


"""
Will go through every row of the CLASSES table and sort them correctly into the
DATA table
"""


class Cleaner:
    def __init__(self):
        self.database = sqlite3.connect(DATABASE_PATH)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()

    def clean(self):
        print('Begin cleaning database.')
        curr_time = time.time()
        self.setup_database()
        self.create_subclass_databases()
        # self.create_links()
        # self.validate_database()
        self.close()
        fin_time = time.time()
        print('Finished cleaning database in {} seconds'.format(fin_time - curr_time))

    """
    Setup database
    """

    def setup_database(self):
        self.cursor.execute('DROP TABLE IF EXISTS DATA')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS DATA '
            '(ID INTEGER PRIMARY KEY, COURSE_NUM TEXT, '
            'LECTURE_KEY INTEGER, LAB_KEY INTEGER, '
            'DISCUSSION_KEY INTEGER, SEMINAR_KEY INTEGER, FINAL_KEY INTEGER)'
        )

    def create_subclass_databases(self):
        course_types = []
        self.cursor.execute("SELECT ID, COURSE_NUM, COURSE_ID, TYPE, DAYS FROM CLASSES")
        courses = self.cursor.fetchall()
        for course in courses:
            viewing_dict = dict(course)
            course_type = str(course['TYPE'])
            if course_type not in course_types and course_type.isupper():
                course_types.append(course_type)
            if not course_type.isupper() or len(course_type) == 0:
                continue
            #self.cursor.execute("DROP TABLE IF EXISTS {}_SUBCLASS".format(course_type))
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {}_SUBCLASS"
                                "(COURSE_NUM TEXT, COURSE_ID TEXT, {}_KEY INTEGER, UNIQUE({}_KEY, COURSE_ID))"
                                .format(course['TYPE'], course['TYPE'], course['TYPE']))
            try:
                self.cursor.execute("INSERT INTO {}_SUBCLASS VALUES(?, ?, ?)".format(course_type),
                                    (course['COURSE_NUM'], course['COURSE_ID'], course['ID']))
            except sqlite3.IntegrityError:
                pass
            #self.cursor.execute("DROP TABLE IF EXISTS {}_SUBCLASS".format(course_type))


        course_keys = [a + '_KEY' for a in course_types]
        course_keys = ', '.join(map(str, course_keys))

        self.cursor.execute("DROP TABLE IF EXISTS CLASS_LEGEND")

        self.cursor.execute("CREATE TABLE CLASS_LEGEND (COURSE_NUM TEXT, COURSE_ID, {})".format(course_keys))

        for t in course_types:
            self.cursor.execute("INSERT INTO CLASS_LEGEND(COURSE_NUM, COURSE_ID, {}) SELECT * FROM {}".format(t+'_KEY', t+'_SUBCLASS'))


        self.cursor.execute("SELECT * FROM LE_SUBCLASS INNER JOIN DI_SUBCLASS ON LE_SUBCLASS.COURSE_ID = DI_SUBCLASS.COURSE_ID")
        #self.cursor.execute("SELECT * FROM LE_SUBCLASS, DI_SUBCLASS, LA_SUBCLASS WHERE LE_SUBCLASS.COURSE_NUM = DI_SUBCLASS.COURSE_NUM AND DI_SUBCLASS.COURSE_NUM = LA_SUBCLASS.COURSE_NUM")
        test = self.cursor.fetchall()
        for t in test:
            view = dict(t)
            #self.cursor.execute("INSERT OR REPLACE INTO CLASS_LEGEND(COURSE_NUM, COURSE_ID, LE_KEY, DI_KEY)",
             #                   "(view['COURSE_NUM'], view['COURSE_ID'], view['LE_KEY'], view['DI_KEY'])")
            print(view)

    def create_links(self):
        self.cursor.execute("SELECT DISTINCT COURSE_NUM FROM CLASSES")
        class_list = self.cursor.fetchall()
        for course_num in class_list:
            self.cursor.execute("SELECT ID, COURSE_ID, DAYS, TYPE "
                                "FROM CLASSES WHERE COURSE_NUM = ?"
                                "ORDER BY ID", course_num)

            """
                The strategy here is to loop through each class database set (Every class that has the same 
                course num), and then if it is a lecture, create a new row inside the database with the
                lab, discussion, and final keys not filled up 
                
                As we continue to loop through the set of database, we will encounter the corresponding
                extra classes (the matching discussion section and such), and we will go to our table, 
                find all the classes with the same course num that don't have any values for the section,
                and populate it with the correct key.
                
                This is how we deal with discussions, labs, and finals sometimes matching to multiple lectures.
            """

            for class_info in self.cursor.fetchall():
                print(str(course_num + class_info))
                # Make sure class is usable
                # TODO Make the below part dynamic
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
            print('*' * 10)

    """
    Make sure that there are no rows where every class (not including final) is null.
    """

    def validate_database(self):
        print('Begin validating database.')
        curr_time = time.time()
        self.cursor.execute(
            'DELETE FROM DATA WHERE COURSE_NUM ISNULL OR LECTURE_KEY ISNULL AND DISCUSSION_KEY ISNULL '
            'AND SEMINAR_KEY ISNULL AND LAB_KEY ISNULL')
        fin_time = time.time()
        print('Finished validating database in {} seconds.'.format(fin_time - curr_time))

    def close(self):
        self.database.commit()
        self.database.close()
