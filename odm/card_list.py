from mongoengine import Document, StringField,  IntField,  DateField, ReferenceField
from datetime import date
from odm.project import Project

class Card_List(Document): 
    meta = {"collection" : "card_list"}

    topic = StringField(max_length=64)
    created_date = DateField( default = date.today())
    starting_date = DateField(null= True) # baslangic ve bitis tarihi planlanmamissa null
    complated_date = DateField(null= True)
    status = IntField()  # alindi : 0 | baslandi : 1| kontrolde : 2 | tamamlandı : 3
    ref_project = ReferenceField(Project , dbref = True, reverse_delete_rule= 2) #  CASCADE    (2)  - Deletes the documents associated with the reference.

    # TODO: atanmis kisiler