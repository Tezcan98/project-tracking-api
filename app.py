from flask import Flask, render_template, request, jsonify, session, redirect, url_for, sessions
from flask_session import Session
from db_procs import *

app = Flask(__name__)
from config import *

Session(app)

@app.route("/")
def index():
	return render_template("dashboard.html")

if __name__ == "__main__":
	app.run(static_url_path='', static_folder='static', template_folder='templates', host='0.0.0.0')
	
