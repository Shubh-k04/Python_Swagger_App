import json
from pymongo import MongoClient
from configs.config import logger
from bson.json_util import dumps
from bson.json_util import loads
from datetime import datetime

class Database:
    """
    A class for handling MongoDB database connections.
    """

    # MongoDB connection string
    CONNECTION_STRING = "mongodb://localhost:27017/logs_injestor"
    COLLECTION_NAME = "logs_db"
    TIME_REGEX = ["%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d", "%Y-%m", "%Y", "%Y-%m-%dT", "%Y-%m-%dT%H", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"]

    def __init__(self):
        """
        Initialize the Database class and establish a MongoDB connection.
        """
        self.client = MongoClient(Database.CONNECTION_STRING)
        self.db = self.client['logs_injestor']

    def get_collection(self):
        """
        Return the desired collection from the database.
        """
        return self.db[Database.COLLECTION_NAME]
    
    def insert_item(self, items):
        """
        Insert new documents into the collection.
        """
        collection = self.get_collection()

        # Convert timestamp strings to datetime objects
        for item in items:
            if "timestamp" in item and isinstance(item["timestamp"], str):
                item["timestamp"] = datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

        # Insert the modified items
        result = collection.insert_many(items)

    def filter_log(self, field: str, value: str = None, regex: str = None):
        """
        Filter items from the collection.
        """
        if regex == 'None':
            logger.info("Checking if the regex: {} exists in the collection".format(regex))
            logger.info("Filtering logs by field: {} and value: {}".format(field, value))
            result = self.get_collection().find({field: value}, {'_id': 0})
        else:
            result = self.get_collection().find({field: {"$regex": regex}}, {'_id': 0})

        result_list = []
        for i in result:
            result_list.append(i)
        return result_list
    
    def filter_logs_by_timestamp_range(self, start_datetime: str, end_datetime: str):
        """
        Filter logs from the collection based on timestamp range.
        """
        logger.info("Filtering logs by start_datetime: {} and end_datetime: {}".format(start_datetime, end_datetime))
        start_timestamp = self.datetime_to_str(start_datetime)
        end_timestamp = self.datetime_to_str(end_datetime)
        
        result = self.get_collection().find({
            "timestamp": {
                "$gte": start_timestamp,
                "$lte": end_timestamp
            }
        }, {'_id': 0})
        
        result_list = []
        for i in result:
            result_list.append(i)
        return result_list
    
    def datetime_to_str(self, date_time):
        """
        Convert date time to string format.
        """
        # convert 2023-11-17T17:11:09.265Z to string using datetime
        for pattern in Database.TIME_REGEX:
            try:
                return datetime.strptime(date_time, pattern)
            except ValueError:
                pass

        raise ValueError("Timestamp does not match any expected format")
    
    def datetime_to_isoformat(self, date_time):
        """
        Convert date time to isoformat.
        """
        return date_time.isoformat()