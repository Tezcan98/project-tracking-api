from email.policy import default
from importlib.resources import contents
from mongoengine import Document, StringField,  IntField,  DateField, ReferenceField, ObjectIdField
from datetime import date
from odm.project import Project
from odm.user import User
from bson import ObjectId

class Card(Document): 
    meta = {"collection" : "cards"}
    _id = ObjectIdField(primary_key=True, default = ObjectId )
    topic = StringField(max_length=64)
    content = StringField(max_length=512, default = "")
    created_date = DateField( default = date.today())
    starting_date = DateField(null= True) # baslangic ve bitis tarihi planlanmamissa null
    complated_date = DateField(null= True)
    status = IntField(default = 0)  # default : 0 | alindi : 1 | baslandi : 2| kontrolde : 3 | tamamlandı : 4
    ref_project = ReferenceField(Project ,reverse_delete_rule= 2) #rule : cascade 
    assignment = ReferenceField(User , reverse_delete_rule= 1) # rule : set null if user delete

    def __init__(self, topic, **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        self.topic = topic
        self.assignment = None
        self.ref_project = None
        self.starting_date = None
        self.complated_date = None

    def add_ref(self, project):
        self.ref_project = project