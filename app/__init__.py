from flask import Flask
from flask_cors import CORS
from flask_restful import Resource,Api

from flask_pymongo import PyMongo


blogapp= Flask(__name__)

blogapp.secret_key = "secret key"

blogapp.config["MONGO_URI"] = "mongodb://localhost:27017/roytuts"

mongo = PyMongo(blogapp)

api=Api(blogapp)
CORS(blogapp)



 
from app.views import super_admin_api,sab_lends_app_api
