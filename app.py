from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from odm.schemas import *
from db_connect import *
from user_processes import user_processes

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['PROPAGATE_EXCEPTIONS'] = True

app.register_blueprint(user_processes)

@app.route("/")
def dashboard():
	return render_template("dashboard.html")

if __name__ == "__main__":
	app.run()
	
