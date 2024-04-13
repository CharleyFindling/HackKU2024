import os

from flask import Flask, render_template
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
##from flask_bcrypt import Bcrypt
##from flask_jwt_extended import JWTManager

from bson import json_util, ObjectId
from datetime import datetime, timedelta
from flask import Blueprint
import api.db as db
from flask import Blueprint, request, jsonify
import api.db as db

from flask_cors import CORS
from datetime import datetime



food_api_v1 = Blueprint(
    'food_api_v1', 'food_api_v1', url_prefix='/api/v1/food')

CORS(food_api_v1)