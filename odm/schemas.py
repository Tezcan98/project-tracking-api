import models
from marshmallow import Schema
import marshmallow_mongoengine as ma

class User_Schema(Schema):
    class Meta:
        model = models.User

class Project_Schema(Schema):
    class Meta:
        model = models.Project

class Card_List_Schema(Schema): 
    class Meta:
        model = models.Card_List
      
class Card_Comment_Schema(Schema): 
    class Meta:
        model = models.Card_Comment