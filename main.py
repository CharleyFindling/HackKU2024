import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os

from flask import Flask, render_template
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
import configparser
##from flask_bcrypt import Bcrypt
##from flask_jwt_extended mport JWTManager
import pymongo
from bson import json_util, ObjectId
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify


def get_db():
    """
    Configuration method to return db instance
    """
    db = pymongo.MongoClient("mongodb+srv://harrisonreed16:7ZMa1gtOuhoBBwyw@foodapp.ruxmkcf.mongodb.net/?retryWrites=true&w=majority&appName=FoodApp")
    db = db['FooApp']
    if db is None:

        db = g._database = PyMongo(current_app).db
        print("DB", db)
       
    return db

class MongoJsonEncoder(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return DefaultJSONProvider.default(obj)


def create_app():
    
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, '/static/')
    TEMPLATE_FOLDER = APP_DIR + '/templates'#os.path.join(APP_DIR, '/templates')
    print(TEMPLATE_FOLDER)

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )
    CORS(app)
    app.json_encoder = MongoJsonEncoder
    #app.register_blueprint(food_api_v1)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('/index.html')

    #db.add_restuarant("NONE" , "NONE", "NONE", "NONE")

    return app
config = configparser.ConfigParser()
config.read('config/.ini')
app = create_app()
app.config['DEBUG'] = True
app.config['MONGO_URI'] = config['PROD']['DB_URI']
# Use LocalProxy to read the global db instance with just `db`
######################### Handleing ############################
db = LocalProxy(get_db)
def resuarant_push(userName, password, name, address):
    temp = PyMongo(app).db
    print(db.Restuarants.insert_one({'userName':userName, 'password': password, 'Restuarant: ' : name, 'Address: ' : address, 'Food Quantity' : 0}))
    return 0
###################### control flow ############################
@app.route('/<path:path>', methods =['POST'])
def flow_restuarant_push(path):
    
    # = request.args.get('name')
    print("IN")
    userName = request.args.get('uName')
    password = request.args.get('pWord')
    rest = request.args.get('rName')
    address = request.args.get('name')
    try:
        #name = expect(post_data.get('name'), str, 'name')
        #print("result of post", db.add_restuarant(str(post_data), "NONE", "NONE", "NONE"))
        resuarant_push(userName, password, rest, address)
        return 0 #Flask.render_template('submit.html')
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
    
@app.route('/post', methods =['POST'])
def flow_post_push(path):
    
    # = request.args.get('name')
    print("IN")
    userName = request.args.get('uName')
    password = request.args.get('pWord')
    rest = request.args.get('rName')
    address = request.args.get('name')
    try:
        #name = expect(post_data.get('name'), str, 'name')
        #print("result of post", db.add_restuarant(str(post_data), "NONE", "NONE", "NONE"))
        resuarant_push(userName, password, rest, address)
        return 0 #Flask.render_template('submit.html')
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
################################################################




if __name__ == "__main__":
    
    
    #get_db()
    app.run()
    #uri = "mongodb+srv://harrisonreed16:7ZMa1gtOuhoBBwyw@foodapp.ruxmkcf.mongodb.net/?retryWrites=true&w=majority&appName=FoodApp"
