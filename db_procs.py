import os
from mongoengine import connect

connect(
db='Project',
host='192.168.56.1',
port=27017,
username='admin',
password= '123',
authentication_source='admin'
)
