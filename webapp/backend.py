from flask import Flask, request, jsonify
import sqlite3
import classpicker
from classutil.class_decoders import ClassDecoder
from settings import DATABASE_PATH

cp = classpicker.ClassPicker()

db_connection = sqlite3.connect(DATABASE_PATH)
db_cursor = db_connection.cursor()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/data', methods=['POST'])
def return_db_data():
    classes = request.json['classes']
    ret_classes = [cp.generate_class_versions(i) for i in classes]

    cd = ClassDecoder()

    ret = [[cd.default(j) for j in i] for i in ret_classes]
    return {ret}


if __name__ == '__main__':
    app.run()
