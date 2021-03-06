from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField, ObjectIdField, ListField
from datetime import date
import json
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document): 
    meta = {"collection" : "users"}
    _id = ObjectIdField(primary_key=True, default = ObjectId )
    email = EmailField(required=True, unique=True)
    name = StringField(max_length=32) 
    password = StringField(max_length=128)

    def __init__(self, email, name, password, **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        self.email = email
        self.name = name
        self.password = password  
    
    def set_hashed_password(self):
        self.password = generate_password_hash(self.password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_password(self):
        return 

    # def get_json(self):
    #     self_dict = '{"_id" :"' + self._id +'", "email" :"'+ self.email +'", "name": "'+self.name +'", "password": "'+ self.password + '"}'
    #     return json.loads(self_dict)