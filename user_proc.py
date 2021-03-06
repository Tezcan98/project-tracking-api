from flask import Blueprint, request, jsonify, session
from flask_session import Session
from mongoengine.errors import NotUniqueError
from odm.schemas import User, User_Schema

user_proc = Blueprint('user_process', __name__)
			
@user_proc.route("/api/register", methods= ["POST"])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	name = request.json.get('name')
	if email is None or password is None or name is None:
		return jsonify({ 'response' : 409, 'message' : "some values are missing."})
	try:
		user = User(email,name, password)
		user.set_hashed_password()
		user.save()
		return jsonify({ 'response': 201, 'message': User_Schema().dump(user) } ) 
	except NotUniqueError as e:
		return jsonify({ 'response' : 409, 'message' : "This e-mail is already registered"})

def verify_password(username, password):
	user = User.objects(email = username).first()
	if len(user) > 0:
		if user.verify_password(password):
			session['user'] = User_Schema().dump(user)
			return True
	else:
		return False

@user_proc.route("/api/verify", methods= ["POST"])
def verify():
	input_email = request.json.get('email')
	password = request.json.get('password')
	if verify_password(input_email, password):
		return jsonify({'response': 200 , 'message':session['user']})	
	return jsonify({'response': 404 , 'message': "Email or Password is wrong. "})

@user_proc.route("/api/logout", methods = ["POST"]) 
def logout(): 
	session.pop('user')
	return jsonify(200)