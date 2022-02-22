from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, sessions

from flask_session import Session
from odm.schemas import *
from db_proc import *
from user_proc import user_proc, Session
from project_proc import project_proc
from card_procs import card_procs


app = Flask(__name__, static_url_path='', static_folder='static')
app.config['PROPAGATE_EXCEPTIONS'] = True

app.register_blueprint(user_proc )
app.register_blueprint(project_proc )
app.register_blueprint(card_procs)

# app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME "] = timedelta(minutes= 30)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def dashboard():
	return render_template("dashboard.html")


@app.route('/api/token', methods = ["POST"]) 
def get_auth_tokend(): 
    return jsonify({ 'token': session['user']})


if __name__ == "__main__":
	app.run()
	
