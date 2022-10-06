from flask import jsonify
from itsdangerous import json
from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.db4

class Database:
    def add_user(self, user):
        db.users.insert_one(user)

    def get_user(self, id):
        cur = db.users.find({"_id": id})
        # print(cur)
        movies = []
        for i in cur:
            movies = i['movies']
        return movies

    def add_movie(self, _id, movie):
        db.users.update({"_id": _id}, {'$push': {"movies": movie}})