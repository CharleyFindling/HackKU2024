from api.myApp import create_app
import api.myApp as api
import configparser
import api.db as db
import api.paths
from flask import Flask
from bson import json_util, ObjectId
from datetime import datetime, timedelta
from flask import Blueprint
import api.db as db
from flask import Blueprint, request, jsonify
import api.db as db

config = configparser.ConfigParser()
config.read('config/.ini')
app = create_app()
app.config
app.config['DEBUG'] = True
current_app = app
app.config['MONGO_URI'] = config['PROD']['DB_URI']

@app.route('/<path:path>', methods=["POST"])
def api_add_restuarant(path):
    post_data = request.args.get('name')
    print("IN")
    try:
        #name = expect(post_data.get('name'), str, 'name')
        print("result of post", db.add_restuarant(str(post_data), "NONE", "NONE", "NONE"))
        return Flask.render_template('submit.html')
    except Exception as e:
        print("Error", e)
        return jsonify({'error': str("DARN")}), 400

if __name__ == "__main__":
    
    
    app.run(debug=True)
    #with app.app_context():
        #print(db.add_restuarant("NONE" , "NONE", "NONE", "NONE"))
    

    
def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    raise AssertionError("Invalid input for type", field)

    
"""
from flask import Flask, render_template, request, redirect, session
 
app = Flask(__name__)
 
# To render a login form 
@app.route('/')
def view_form():
    return "hello world"

@app.route('/handle_get', methods=['GET'])
def handle_get():
    return "hello from get method
    """