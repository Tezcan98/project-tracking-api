from odm.models import *
from marshmallow_mongoengine import ModelSchema

class User_Schema(ModelSchema):
    class Meta:
        model = User

class Project_Schema(ModelSchema):
    class Meta:
        model = Project

class Card_List_Schema(ModelSchema): 
    class Meta:
        model = Card_List
      
class Card_Comment_Schema(ModelSchema): 
    class Meta:
        model = Card_Comment