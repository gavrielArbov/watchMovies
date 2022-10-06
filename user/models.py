from flask import Flask, jsonify, request
import uuid

from database import Database

db = Database()

class User:
	def signup(self):
		user = {
			"_id": uuid.uuid4().hex,
			"username": request.form.get("username"),
			"first_name": request.form.get("first_name"),
			"last_name": request.form.get("last_name"),
			"email": request.form.get("email"),
			"password": request.form.get("password"),
			"movies": []
			}
		db.add_user(user)
		return user["_id"]

	def get_user(self, id):
		return db.get_user(id)

	def add_movie(self, id, movie):
		db.add_movie(id, movie)