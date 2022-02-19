from mongoengine import Document, StringField, EmailField, IntField, BooleanField, DateField, ReferenceField
from datetime import date

class User(Document):
    id = IntField(Required = True, unique = True)
    email = EmailField(required=True, unique=True)
    first_name = StringField(max_length=32)
    last_name = StringField(max_length=32)
    password = StringField(max_length=32)

class Project(Document):
    id = IntField(Required = True, unique = True)
    name = StringField(max_length=64)
    status = BooleanField(required= True, default= True)
    created_date = DateField( default = date.today())
    # TODO: yetkili
 
class Card_List(Document):
    id = IntField(Required = True, unique = True)
    topic = StringField(max_length=64)
    created_date = DateField( default = date.today())
    starting_date = DateField(null= True) # baslangic ve bitis tarihi planlanmamissa null
    complated_date = DateField(null= True)
    status = IntField()  # alindi : 0 | baslandi : 1| kontrolde : 2 | tamamlandı : 3
    ref_project = ReferenceField(Project , dbref = True, reverse_delete_rule= 2) #  CASCADE    (2)  - Deletes the documents associated with the reference.

    # TODO: atanmis kisiler
  
class Card_Comment(Document):
    id = IntField(Required = True, unique = True)
    text = StringField(max_length=512)
    created_date = DateField( default = date.today(), null= True)
    ref_project = ReferenceField(Card_List , dbref = True, reverse_delete_rule= 2)  
    # TODO: gonderen idsi