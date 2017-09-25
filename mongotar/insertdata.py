from argument import host, port, user, passwd, query, backpath, db, backfile, backupcmd, restorecmd, collection,key
from pymongo import MongoClient




def insert_data():
    client = MongoClient(host, port)
    dbc = client.get_database(db)
    dbc.authenticate(user, passwd)
    table = dbc.get_collection(collection)
    table.insert({'txDate':'20170310'})
    client.close()