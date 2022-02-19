from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from mongoengine.errors import NotUniqueError
from odm.models import *
from db_connect import *

from werkzeug.security import generate_password_hash, check_password_hash 

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_marshmallow import Marshmallow

app = Flask(__name__, static_url_path='',
            static_folder='static')
 
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
@app.route("/index")
def dashboard():
	return render_template("dashboard.html")
 
	
@app.route("/register/<email>", methods= ["PUT"])
def register(email):
	try:
		user = User(email,"enes","tezcan", "password") 
		user.save()
		
	except NotUniqueError as e:
		return jsonify(-1)
	
	return jsonify(str(user.id))

if __name__ == "__main__":
	app.run()
	
