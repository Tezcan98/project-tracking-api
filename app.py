from flask import Flask, render_template, request, jsonify, session, redirect, url_for, sessions
from flask_session import Session
from db_procs import *

app = Flask(__name__,  static_url_path='', static_folder='static', template_folder='templates')

from config import configs

configs(app)
Session(app)

@app.route("/")
def index():
	port = request.environ.get('REMOTE_PORT')
	return "Hello docker on port : " + str(port)
	# return render_template("dashboard.html")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
	
