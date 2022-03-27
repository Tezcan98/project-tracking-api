# from app import app
from datetime import timedelta
import os
from user_proc import user_proc
from project_proc import project_proc
from card_procs import card_procs
from comment_procs import comment_proc
from mail_service import mail_service
from mailadress import address, password

def configs(app):
    app.register_blueprint(user_proc )
    app.register_blueprint(project_proc )
    app.register_blueprint(card_procs)
    app.register_blueprint(comment_proc)
    app.register_blueprint(mail_service)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    # app.config["SESSION_PERMANENT"] = False
    app.config["PERMANENT_SESSION_LIFETIME "] = timedelta(minutes= 30)
    app.config["SESSION_TYPE"] = "filesystem"


    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = address
