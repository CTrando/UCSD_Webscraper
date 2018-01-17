import psycopg2
import sqlite3

from settings import DATABASE_PATH

db_connection = sqlite3.connect(DATABASE_PATH)
db_cursor = db_connection.cursor()

db_cursor.execute("SELECT * FROM CLASS_LEGEND")
column_names = [descriptions[0] for descriptions in db_cursor.description]
column_insert_str = ', '.join(column_names)
column_create_str = ' TEXT,'.join(column_names) + ' TEXT'

copy_connection = psycopg2.connect(dbname="copy",
                                   user="postgres",
                                   password="ctrando",
                                   host="localhost",
                                   port=5432)

copy_cursor = copy_connection.cursor()
copy_cursor.execute("DROP TABLE IF EXISTS DATA")
copy_cursor.execute("CREATE TABLE DATA ""({})".format(column_create_str))

data = db_cursor.fetchall()

for tup_val in data:
    copy_cursor.execute("INSERT INTO DATA ({}) VALUES({})"
                        .format(column_insert_str, ("%s," * len(tup_val))[:-1]),  tup_val)

copy_connection.commit()
copy_cursor.close()
copy_connection.close()



