from odm.card import Card
from odm.comment import Comment
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
      
class Comment_Schema(ModelSchema): 
    class Meta:
        model = Comment