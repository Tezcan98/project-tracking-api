from mongoengine import Document, StringField,  IntField,  DateField, EmailField, ObjectIdField
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class Mail(Document):  # Storage system mail
    meta = {"collection" : "mail"}
    _id = ObjectIdField(primary_key=True, default = ObjectId )
    address = EmailField(required=True, unique=True)
    password = StringField(max_length=128)

    def __init__(self, address, password , **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        self.address = address
        self.password = password

    def set_hashed_password(self):
        self.password = generate_password_hash(self.password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)