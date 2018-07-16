from pymongo import MongoClient
from flask import Flask

application = Flask(__name__)

from routes import *

if __name__ == "__main__":
    application.run()

