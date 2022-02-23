from mongoengine import connect

connect(
db='iq_project',
host='localhost',
port=27017,
username='',
password='',
authentication_source='admin'
)
