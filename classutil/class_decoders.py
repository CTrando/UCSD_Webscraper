from classutil.classutils import Class, Subclass
from flask import jsonify
import json


class ClassDecoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, Class):
            return ValueError("Not the correct type")

        subclass_decoder = SubClassDecoder()
        subclass_str = ''
        for i in o.subclasses.values():
            subclass_str += subclass_decoder.default(i)
        return subclass_str


class SubClassDecoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, Subclass):
            return ValueError("Not the correct type")

        return json.dumps(o.data)
