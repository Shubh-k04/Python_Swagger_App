import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")
