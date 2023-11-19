# Create a function to filter logs by timestamp range
from flask import jsonify
from configs.config import logger
from flask_restful import Resource
from utils.database.setup import Database
from json import dumps, loads


class FilterLogsByTimestampRange(Resource):
    """
    Filter logs from the collection based on timestamp range provided by the user.
    """
    def jsonify_datetime_list(self, datetime_list):
        """
        Custom function to jsonify a list of dictionaries containing datetime objects.
        """
        # Convert datetime objects to string format
        for item in datetime_list:
            if 'timestamp' in item:
                item['timestamp'] = item['timestamp'].isoformat()

        return datetime_list
    
    def get(self, start_datetime, end_datetime):
        """
        Gets the logs from the collection based on timestamp range provided by the user.
        """
        # Validate input parameters
        if not start_datetime or not end_datetime:
            return jsonify({'error': 'Invalid input parameters'}), 400

        # Filter logs by timestamp range
        db = Database()
        result_list = db.filter_logs_by_timestamp_range(start_datetime, end_datetime)
        # Return the filtered logs
        return loads(dumps(self.jsonify_datetime_list(result_list))), 200
    