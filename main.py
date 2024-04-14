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
from bson import json_util
import json

#Name: get_deb
#Description: creates a "link" to the data-base, as db
#####################Create Database##############################
def get_db():
    """
    Configuration method to return db instance
    """
    db = pymongo.MongoClient("mongodb+srv://harrisonreed16:7ZMa1gtOuhoBBwyw@foodapp.ruxmkcf.mongodb.net/?retryWrites=true&w=majority&appName=FoodApp")
    db = db['FooApp']['db']
    if db is None:

        db = g._database = PyMongo(current_app).db
        print("DB", db)
       
    return db

#Name: MongoJsonEncoder
#Description: Creates the Json encoder for the mongo data-base
class MongoJsonEncoder(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return DefaultJSONProvider.default(obj)
    
#Name: create_app
#Description: Creates the application by assigning various values to a newly created flask app
#Return: returns the new app
########################Create App##############################
def create_app():
    
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, '/static/')
    TEMPLATE_FOLDER = APP_DIR + '/templates'
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
    return app
###############################################################
#Create config parser
config = configparser.ConfigParser()
config.read('config/.ini')

#Create the application, and assign configuration
app = create_app()
app.config['DEBUG'] = True
app.config['MONGO_URI'] = config['PROD']['DB_URI']

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

#Description: Does work when on corresponding HTML methods
######################### Handling ############################
def restuarant_push(userName, password, isBusiness,isIndividual,isOrg, name,driversLicense, dob, address):
    temp =  {"db":{
            "Entity":[
            {
                "userName": str(userName),
                "password": str(password),
                "isBusiness": bool(isBusiness),
                "isIndividual": bool(isIndividual),
                "isOrg": bool(isOrg),
                "Name": str("Hello"),
                "location": str(address),
                "driversLicense": str(driversLicense),
                "dob": str(dob)
            }
        ],

        "food": [
            {
                "foodId": 0,
                "foodName": "",
                "foodBestBy": "",
                "foodQuantity": 0,
                "foodPostedBy": "",
                "foodLocation": "",
                "pickUpTime": ""
            }
        ]
    }
    }
    #{str(userName):[{'password': password, 'Restuarant: ' : name, 'Address: ' : address}]}
    print(db.insert_one(temp))

def food_push(foodId, foodName, foodBestBy, foodQuantity, foodPostedBy, foodLocation, pickUpTime):

    if(foodId == None):
        foodId = 0

    template = {
                "foodId": foodId,
                "foodName": foodName,
                "foodBestBy": foodBestBy,
                "foodQuantity":foodQuantity,
                "foodPostedBy": foodPostedBy,
                "foodLocation": foodLocation,
                "pickUpTime": pickUpTime
                }
    
    print("\n\n",db.update_many({"db.Entity.Name" : "Hello"}, {"$set": {"db.food": template}}, upsert=True))

##NOT DONE YET
def food_update(foodId):
    print(db)
    result = []
    temp = db.find({"db.food.foodId" : 0})

        
    result = json.loads(json_util.dumps(temp))
    result = list(result)
    #print(map(result[0][1]))
    #print("Len", len(result[0][1]))
    #for i in range(len(result)):
        #for j in range(len(result[i])):
            #if(result[i][j] == 'foodQuantitiy'):
                #foodQuantity = result[i][j][0]
    foodQuantity = 0
    if(foodQuantity > 0):
        foodQuantity -= 1
        db.update_one({"db.food.foodId": 0},

               {"$set":{
                "db.food.foodQuantity": foodQuantity
                }
                      }
    
        )
        if(foodQuantity==0):
            deleteFoodByID(foodId)
    
    

#Name: getAllFoodNearby
#Description: Retrieves all elemnts that are near the current distance
#Param: thisDistance - the distance to compare against
def getAllFoodNearby(thisDistance):
    result = []
    curser = db.find({"db.Entity.distance": {"$gt": thisDistance, "$lt": thisDistance}})
    result = json.loads(json_util.dumps(curser))
    print(result)
    return result

#Name: getByBusiness
#Description: Retrieves the element in the data base that contains the business name
#Param: businessName - the name to be retrieved
def getByBusiness(bussinessName):
    print("By business")
    result = []
    temp = db.find({"db.Entity.Name" : bussinessName})
    result = json.loads(json_util.dumps(temp))

    return result


#Name: getByFoodID
#Description: Retrieves the element in the data base that contains the food element
#Param: thisID - the id to be retrieved
def getByFoodId(thisId):
    result = []
    temp = db.find({"db.food.foodId" : thisId})
    result =json.loads(json_util.dumps(temp))

    print(result)
    return result


#Name: deleteFoodByID
#Description: Deletes item contained in the data base based on the foods id number
#Useful for when food becomes "out of stock"
#Param: thisID - the id to be deleted
def deleteFoodByID(thisID):
    if(db.find_one({"db.food.foodId" : thisID})):
        db.delete_one({"db.food.foodId" : thisID})
    else:
        return "Element not in db"
    
def getAll():
    result = []
    cursor = db.find({})
    for document in cursor:
          result.append(json_util.dumps(document))
    return result
#Description: Control flow section to handle HTML methods
###################### control flow ############################
@app.route('/get_all', methods=['GET'])
def flow_get_all():
    try:
        return (getAll())
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
    

@app.route('/restuarant_push', methods =['POST'])
def flow_restuarant_push():
    
    #ADD WHEN READY 
    userName = request.args.get('uName')
    password = request.args.get('pWord')
    print(userName)
    isBusiness = request.args.get('isBusiness')
    isIndividual = request.args.get('isIndividual')
    isOrg = request.args.get('isOrg')
    name = request.args.get('rName')
    address = request.args.get('name')
    driversLicense = request.args.get('driversLicense')
    dob = request.args.get('dob')
    try:
        restuarant_push(userName, password, isBusiness,isIndividual,isOrg, name,driversLicense, dob, address)
        return ("restuarant push")
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
    
@app.route('/food_push', methods=['POST'])
def flow_food_push():
    foodId = request.args.get('foodId')
    foodName = request.args.get('foodName')
    foodBestBy = request.args.get('foodBestBy')
    foodQuantity = request.args.get('foodQuantity')
    foodPostedBy = request.args.get('foodPostedBy')
    foodLocation = request.args.get('foodLocation')
    pickUpTime = request.args.get('pickUpTime')
    try:
        food_push(foodId, foodName, foodBestBy, foodQuantity, foodPostedBy, foodLocation, pickUpTime)
        return ("food push") #render_template('submit.html')
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400

@app.route('/food_update', methods=['POST'])
def flow_food_update():
    foodId = request.args.get('foodId')
    foodQuantity = request.args.get('foodQuantity')
    try:
        food_update(foodId)#foodQuantity)
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
    
#Name:flow_byBusiness_get
#Description: Calls the getByBusinessfunction when,
#Directory of app is appended by /byBusiness and A GET call is made  
@app.route('/byBusiness', methods=['GET'])
def flow_byBusiness_get():
    business = request.args.get('business')
    try:
        return getByBusiness("Hello")
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400

#Name:flow_getByFoodId
#Description: Calls the getByFoodId function when,
#Directory of app is appended by /byFoodId and A GET call is made     
@app.route('/byFoodId', methods=['GET'])
def flow_getByFoodId_get():
    fID = request.args.get('foodID')
    try:
        return getByFoodId(fID)
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400

#Name:flow_deleteFood_delete
#Description: Calls the delete by food function when,
#Directory of app is appended by /delete and A DELETE call is made 
@app.route('/delete', methods=['DELETE'])
def flow_deleteFood_delete():
    fID = request.args.get('foodID')
    try:
        return deleteFoodByID(fID)
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400
################################################################



# Name: main
# Description: Starts the application
if __name__ == "__main__":
    app.run()
    
