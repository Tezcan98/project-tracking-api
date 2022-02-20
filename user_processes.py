from queue import Empty
from flask import Blueprint, request, jsonify
from mongoengine.errors import NotUniqueError
from odm.schemas import *
import json

#TODO: hashing password 
from werkzeug.security import generate_password_hash, check_password_hash

user_processes = Blueprint('user_process', __name__)

	
@user_processes.route("/api/register", methods= ["POST"])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	name = request.json.get('name')

	if email is None or password is None or name is None:
		return jsonify(400)
	try:
		hashed_password = generate_password_hash(password)
		
		user = User( email,name, hashed_password)
		user.save()  
		json_user = User_Schema()
		return json_user.dump(user)
	except NotUniqueError as e:
		return jsonify(400)

@user_processes.route("/api/verify", methods= ["POST"])
def verify_password():
	input_email = request.json.get('email')
	password = request.json.get('password')
	loaded_user = User.objects(email = input_email)

	if loaded_user.count() == 1:
		if check_password_hash(loaded_user.first().password, password):
			user = loaded_user().first()
			json_user = User_Schema()
			# return json_user.load(user.get_json())
			return user.get_json()
	return jsonify(404) 