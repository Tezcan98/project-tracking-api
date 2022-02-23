from email.policy import default
from importlib.resources import contents
from mongoengine import Document, StringField,  IntField,  DateField, ReferenceField, ObjectIdField
from datetime import datetime
from odm.project import Project
from odm.user import User
from bson import ObjectId

class Card(Document): 
    meta = {"collection" : "cards"}
    _id = ObjectIdField(primary_key=True, default = ObjectId )
    topic = StringField(max_length=64)
    content = StringField(max_length=512, default = "")
    created_date = DateField( default = datetime.utcnow())
    starting_date = DateField(null= True)
    complated_date = DateField(null= True)
    status = IntField(default = 0)  # default : 0 | alindi : 1 | baslandi : 2| kontrolde : 3 | tamamlandı : 4
    ref_project = ReferenceField(Project , default = None ,reverse_delete_rule= 2) #rule : cascade 
    assignment = ReferenceField(User ,default = None , reverse_delete_rule= 1) # rule : set null if user delete

    def __init__(self, topic, **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        if 'ref_project' in values:
            self.ref_project = values['ref_project']
        self.topic = topic
        self.assignment = None
        self.starting_date = None
        self.complated_date = None

    def add_ref(self, project):
        self.ref_project = project

    def check_project_auth(self, user_id):
        return user_id in self.ref_project.auth_users
