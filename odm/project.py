from email.policy import default
from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField, ObjectIdField, ListField
from datetime import date
from odm.user import User
from random import randint
class Project(Document): 
    meta = {"collection" : "projects"}
    _id = ObjectIdField()
    name = StringField(max_length = 64, unique = True)
    status = BooleanField(required = True, default = True)
    created_date = DateField( required = True, default = date.today())
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

    def delete_auth_user(self, user_mail):
        if user_mail in self.auth_users:
            self.auth_users.remove(user_mail)
            return True
        return False