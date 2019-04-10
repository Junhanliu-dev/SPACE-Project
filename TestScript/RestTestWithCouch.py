import requests
from ANTClient import config
from random import randint
import couchdb

destUrl = config.url + '/active_user/' + '001' + '/heart_rate'
couch_address = "http://admin:liujunhanchang@18.219.29.53:5984/"

def mockHR():
    for i in range(500):
        body = {'id': '001', 'heart_rate': str(randint(50, 60))}
        r = requests.post(url=destUrl, json=body)
        print r.text


def registerSession():

    body = {'message': 'register_session', 'id': '001'}
    r = requests.post(url=config.url + '/register_session', json=body)
    msg = r.text


def deleteDB():

    couch_address = "http://admin:liujunhanchang@18.219.29.53:5984/"
    essential_db = ['_replicator','_users','space_prog', 'space_proj']
    server = couchdb.Server(couch_address)

    for db in server:
        if db not in essential_db:
            server.delete(db)

    for db in server:
        print db


def checkDB():
    couch_address = "http://admin:liujunhanchang@18.219.29.53:5984/"
    server = couchdb.Server(couch_address)
    for db in server:
        print db


server = couchdb.Server(couch_address)
db = server['_users']

for item in db:
    if item not in ['org.couchdb.user:admin', '_design/_auth']:
        del db[item]

