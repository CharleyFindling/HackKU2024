#Backend for hackKU 24, in which the project is a Food collection service

import bson

from flask import Flask
from flask import current_app, g
from app import create_app
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
import config

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId

import configparser

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config/.ini')
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['PROD']['DB_URI']

    app.run()
