from odm.card import Card
from odm.card_comment import Card_Comment
from odm.project import Project
from odm.user import User
from marshmallow_mongoengine import ModelSchema

class User_Schema(ModelSchema):
    class Meta:
        model = User

class Project_Schema(ModelSchema):
    class Meta:
        model = Project

class Card_Schema(ModelSchema): 
    class Meta:
        model = Card
      
class Card_Comment_Schema(ModelSchema): 
    class Meta:
        model = Card_Comment