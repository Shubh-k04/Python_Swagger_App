from flask import request
from configs.config import logger
from flask_restful import Resource
from utils.database.setup import Database

class InsertData(Resource):
    """
    A class for inserting logs into the collection.
    """
    def post(self):
        """
        Insert logs into the collection provided by the user.
        """
        # take input from user
        data = request.get_json()

        if not data:
            logger.warn("Data provided is not in JSON format")
            return 'No JSON data provided', 400
        
        db = Database()
        db.insert_item(data)
        logger.info("Data inserted successfully")
        return "Data inserted successfully", 200
