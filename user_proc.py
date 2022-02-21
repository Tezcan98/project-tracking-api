from flask import Blueprint, request, jsonify, session
from flask_session import Session
from mongoengine.errors import NotUniqueError
from odm.schemas import User, User_Schema
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth() 

user_proc = Blueprint('user_process', __name__)
			
@user_proc.route("/api/register", methods= ["POST"])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	name = request.json.get('name')
	if email is None or password is None or name is None:
		return jsonify(400)
	try:
		hashed_password = generate_password_hash(password)
		user = User(email,name, hashed_password)
		user.save()
		return jsonify({response: 201, message: User_Schema().dump(user) } ) 
	except NotUniqueError as e:
		return jsonify(400)

def verify_password(username, password):
	user = User.objects(email = username).first()
	if len(user) > 0:
		if check_password_hash(user.password, password): 
			session['user'] = User_Schema().dump(user)
			return True
	else:
		return False

@user_proc.route("/api/verify", methods= ["POST"])
def verify():
	input_email = request.json.get('email')
	password = request.json.get('password')
	if verify_password(input_email, password):
		return jsonify(session['user'])	
	return jsonify(404)

@user_proc.route("/api/logout", methods = ["POST"]) 
def logout(): 
	session['user'] = "401"
	return jsonify(200)