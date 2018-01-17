from classutil.classutils import Class, Subclass
from flask import jsonify
import json


class ClassDecoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, Class):
            return ValueError("Not the correct type")

        subclass_decoder = SubClassDecoder()
        subclass = []
        for i in o.subclasses.values():
            subclass.append(subclass_decoder.default(i))
        return subclass


class SubClassDecoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, Subclass):
            return ValueError("Not the correct type")

        return o.data
