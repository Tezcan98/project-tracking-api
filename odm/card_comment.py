from mongoengine import Document, StringField,  IntField,  DateField, ReferenceField
from datetime import date
from odm.card_list import Card_List
  
class Card_Comment(Document): 
    
    meta = {"collection" : "card_comment"}

    text = StringField(max_length=512)
    created_date = DateField( default = date.today(), null= True)
    ref_project = ReferenceField(Card_List , dbref = True, reverse_delete_rule= 2)  
    # TODO: gonderen idsi