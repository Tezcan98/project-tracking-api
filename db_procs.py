import os
from mongoengine import connect

connect(
db='Project',
host='0.0.0.0',
port=27017,
username='admin',
password= '123',
authentication_source='admin'
)
