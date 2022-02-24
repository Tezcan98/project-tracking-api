from mongoengine import connect

connect(
db='flaskdb',
host='mongodb',
port=27017,
username='user',
password='123',
authentication_source='admin'
)
