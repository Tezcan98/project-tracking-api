from mongoengine import Document, StringField,  IntField,  DateField, ReferenceField, ObjectIdField
from datetime import datetime
from odm.card import Card
from odm.user import User
from bson import ObjectId

class Comment(Document): 
    
    meta = {"collection" : "comments"}
    _id = ObjectIdField(primary_key=True, default = ObjectId )
    content = StringField(max_length=512)
    created_date = DateField(default = datetime.utcnow())
    ref_card = ReferenceField(Card ,default = None , reverse_delete_rule= 2)  
    creator_user = ReferenceField(User , default = None ,reverse_delete_rule= 2) #rule : cascade 

    def __init__(self, content = content, **values):
        super().__init__()
        if '_id' in values:
            self._id = str(values['_id'])
        if 'ref_card' in values:
            self.ref_card = values['ref_card']
        if 'creator_user' in values:
            self.creator_users = values['creator_user']
        self.content = content
    
    def set_ref(self, card):
        self.ref_card = card 
    
    def set_creator(self, user):
        self.creator_users = user

    def check_project_auth(self, user_id):
        return user_id in self.ref_card.ref_project.auth_users