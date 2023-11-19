from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import json
from configs.config import app, api, logger
from pkg.filterByTimestamp import FilterLogsByTimestampRange
from pkg.insertLogs import InsertData
from pkg.filterLogs import FilterLogs

api.add_resource(InsertData, '/insert')
api.add_resource(FilterLogs, '/filter')
api.add_resource(FilterLogsByTimestampRange, '/filter/filterByTimestamp/<start_datetime>/<end_datetime>')

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:3000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Log Intake"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    logger.info("Starting the server...")
    app.run(debug=True, port=3000, host='127.0.0.1')

