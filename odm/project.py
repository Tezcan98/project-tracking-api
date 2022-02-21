from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField, ObjectIdField, ListField
from datetime import date
from user import User

class Project(Document): 
    meta = {"collection" : "projects"}
    name = StringField(max_length = 64, unique = True)
    status = BooleanField(required = True, default = True)
    created_date = DateField( required = True, default = date.today())
    user_field = ListField(User, default = [])
    # TODO: yetkili

    def __init__(self, name, **values):
        super().__init__()
        self.name = name

    def add_auth_user(self, user):
        self.user_field.append(user)

    def delete_auth_user(self, user):
        if user in self.user_field:
            self.user_field.remove(user)
            return True
        return False

    def set_activity(self, activity):
        self.status = activity
 