from flask import Flask, Blueprint
from celery import Celery
from flask_mail import Mail

mail_service = Blueprint('mail_service', __name__)

# mail_service.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# mail_service.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# mail = Mail(mail_service)


# celery = Celery(mail_service.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(mail_service.config)

# @mail_service.route("/app/send_mail")
# def index():
#   msg = Message('Hello from the other side!', sender =   'peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
#   msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
#   mail.send(msg)
#   return "Message sent!"



# @celery.task
# def my_background_task(arg1, arg2):
#     # some long running task here
#     return "404"