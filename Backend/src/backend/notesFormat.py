from pymongo import MongoClient
import json

uri = "mongodb+srv://bwajeremiah_db_user:39firehouse@cluster0.hklay79.mongodb.net/"
client = MongoClient(uri)
import time


class Note:
    def __init__(self, text, id, last_edited_date,):
        self.text = text
        self.id = id
        self.last_edited_date = last_edited_date

    def to_dict(self):
        return {
            "text": self.text,
            "id": self.id,
            "last_edited_date": self.last_edited_date   
        }