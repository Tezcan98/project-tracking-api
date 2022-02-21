from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField, ObjectIdField, ListField
from datetime import date
import json

class User(Document): 
    meta = {"collection" : "users"}
    _id = ObjectIdField()
    email = EmailField(required=True, unique=True)
    name = StringField(max_length=32) 
    password = StringField(max_length=128)

    def __init__(self, email, name, password, **values):
    # def __init__(self, *args, **values):
        super().__init__()
        self.email = email
        self.name = name
        self.password = password  
    
    def get_json(self):
        self_dict = '{"email" :"'+ self.email +'", "name": "'+self.name +'", "password": "'+ self.password + '"}'
        return json.loads(self_dict)