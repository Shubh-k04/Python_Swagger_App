from flask import jsonify, request
from configs.config import logger
from flask_restful import Resource
from json import dumps, loads
from utils.database.setup import Database
from datetime import datetime

class FilterLogs(Resource):
    """
    A class for filtering logs from the collection.
    """
    def jsonify_datetime_list(self, datetime_list):
        """
        Custom function to jsonify a list of dictionaries containing datetime objects.
        """
        # Convert datetime objects to string format
        for item in datetime_list:
            if 'timestamp' in item and isinstance(item['timestamp'], datetime):
                item['timestamp'] = item['timestamp'].isoformat()

        return datetime_list

    def get(self):
        """
        Get the logs from the collection based on either:
        - the regex provided for a given field
        - the value provided for a given field
        """
        # Retrieve query parameters
        field_to_filter = request.args.get('field_to_filter')
        value_to_filter = request.args.get('value_to_filter')
        regex_for_filter = request.args.get('regex_for_filter')

        # filter data from the collection
        logger.info("Filtering logs from the collection...")
        db = Database()
        result_list = db.filter_log(field=field_to_filter, value=str(value_to_filter), regex=str(regex_for_filter))
        logger.info("Logs filtered successfully", result_list)

        # Convert datetime objects to string format
        return_json = loads(dumps(self.jsonify_datetime_list(result_list)))

        logger.info("Returning the filtered logs", return_json)
        # Return the string
        return return_json, 200
