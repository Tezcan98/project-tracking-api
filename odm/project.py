from email.policy import default
from tkinter.messagebox import NO
from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField, ObjectIdField, ListField
from datetime import datetime
from odm.user import User
from bson import ObjectId
class Project(Document): 
    meta = {"collection" : "projects"}
    _id = ObjectIdField(primary_key=True, default = ObjectId )
    name = StringField(max_length = 64)
    status = BooleanField(required = True, default = True)
    created_date = DateField( required = True, default = datetime.utcnow())
    auth_users = ListField( field = StringField(), default = [])

    def __init__(self, name, **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        if 'auth_users' in values:
            self.auth_users = values['auth_users']
        self.name = name

    def add_auth_user(self, user_mail):
        self.auth_users.append(user_mail)
    
    def get_status(self):
        return self.status