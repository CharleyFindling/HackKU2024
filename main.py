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
    temp = {str(userName):[{'password': password, 'Restuarant: ' : name, 'Address: ' : address}]}
    print(db.Restuarants.insert_one(temp))


def getAllFoodNearby(thisDistance):
    result = []
    curser = db.find({"distance": {"$gt": thisDistance, "$lt": thisDistance}})
    for curser in curser:
        result.append(curser)
    print(result)
    return result

def getByBusiness(bussinessName):
    print("By business")
    return db.find({"business" : bussinessName})

def getByFoodId(thisId):
    result = []
    curser = db.find({"foodId" : thisId})
    for curser in curser:
        result.append(curser)
    return result

def deleteFoodByID(thisID):
    db.remove({"foodId" : thisID})
    return
###################### control flow ############################
@app.route('/restuarant_push', methods =['POST'])
def flow_restuarant_push(path):
    
    #ADD WHEN READY 
    userName = request.args.get('uName')
    password = request.args.get('pWord')
    print(userName)
    rest = request.args.get('rName')
    address = request.args.get('name')
    try:
        resuarant_push(userName, password, rest, address)
        return ("restuarant push") #render_template('submit.html')
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
    
    
@app.route('/nearby', methods =['GET'])
def flow_nearby_get():
    
    #ADD WHEN READY 
    distance = request.args.get('distance')
    #password = request.args.get('pWord')

    try:
        return "Nearby food" #getAllFoodNearby(int(distance))
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
    

@app.route('/byBusiness', methods=['GET'])
def flow_byBussiness_get():
    business = request.args.get('business')
    try:
        return "busines by id"#getByBusiness(business)
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
    
@app.route('/byFoodId', methods=['GET'])
def flow_getByFoodId_get():
    fID = request.args.get('foodID')
    try:
        return "by food id"#getByFoodId(fID)
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400

@app.route('/delete', methods=['DELETE'])
def flow_deleteFood_delete():
    fID = request.args.get('foodID')
    try:
        return "delete food id"#deleteFoodByID(fID)
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
# ###############################################################




if __name__ == "__main__":
    
    
    #get_db()
    app.run()
    #uri = "mongodb+srv://harrisonreed16:7ZMa1gtOuhoBBwyw@foodapp.ruxmkcf.mongodb.net/?retryWrites=true&w=majority&appName=FoodApp"
