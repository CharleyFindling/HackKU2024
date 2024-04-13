#Backend for hackKU 24, in which the project is a Food collection service


import bson

from flask import Flask
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient


def db_init():
    return 0
    #db = g._database = PyMongo(current_app).db
    

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    client = MongoClient('mongodb://localhost:27017/')
    print(client)
    db = client['FoodApp']
    print("CURRENT APP" , db)
    if db is None:
        
        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def add_restuarant(userName, password ,name, address):
    restuarant_doc = {'userName':userName, 'password': password, 'Restuarant: ' : name, 'Address: ' : address, 'Food Quantity' : 0}
    return db.Restuarants.insert_one(restuarant_doc)
    
def restuarntPost(thisRestuarant, newPost):
    postDoc = [{thisRestuarant:{'recent post ' : newPost}}]
    return db.Posts.insert_one(postDoc)