from flask import Flask, render_template, request, jsonify, session, redirect, url_for, sessions
from flask_session import Session
from db_procs import *

app = Flask(__name__, static_url_path='', static_folder='static')
from config import *

Session(app)

@app.route("/")
def dashboard():
	return render_template("dashboard.html")

if __name__ == "__main__":
	app.run()
	
