from email.policy import default
from mongoengine import Document, StringField,  IntField,  DateField, ReferenceField, ObjectIdField
from datetime import date
from odm.project import Project
from odm.user import User

class Card_List(Document): 
    meta = {"collection" : "card_list"}
    _id = ObjectIdField(primary_key=True)
    topic = StringField(max_length=64)
    created_date = DateField( default = date.today())
    starting_date = DateField(null= True) # baslangic ve bitis tarihi planlanmamissa null
    complated_date = DateField(null= True)
    status = IntField(default = 0)  # default : 0 | alindi : 1 | baslandi : 2| kontrolde : 3 | tamamlandı : 4
    ref_project = ReferenceField(Project , dbref = True, reverse_delete_rule= 2) #rule : cascade 
    assignment = ReferenceField(User , dbref = True, reverse_delete_rule= 1) # rule : set null if user delete

    def __init__(self, topic, project, **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        self.topic = topic
        ref_project = project
        self.assignment = None
        self.starting_date = None
        self.complated_date = None