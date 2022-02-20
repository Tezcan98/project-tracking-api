import email
from enum import unique
from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField, ObjectIdField
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

class Project(Document): 
    meta = {"collection" : "projects"}
    name = StringField(max_length=64)
    status = BooleanField(required= True, default= True)
    created_date = DateField( default = date.today())
    # TODO: yetkili
 
class Card_List(Document): 
    meta = {"collection" : "card_list"}

    topic = StringField(max_length=64)
    created_date = DateField( default = date.today())
    starting_date = DateField(null= True) # baslangic ve bitis tarihi planlanmamissa null
    complated_date = DateField(null= True)
    status = IntField()  # alindi : 0 | baslandi : 1| kontrolde : 2 | tamamlandı : 3
    ref_project = ReferenceField(Project , dbref = True, reverse_delete_rule= 2) #  CASCADE    (2)  - Deletes the documents associated with the reference.

    # TODO: atanmis kisiler
  
class Card_Comment(Document): 
    
    meta = {"collection" : "card_comment"}

    text = StringField(max_length=512)
    created_date = DateField( default = date.today(), null= True)
    ref_project = ReferenceField(Card_List , dbref = True, reverse_delete_rule= 2)  
    # TODO: gonderen idsi