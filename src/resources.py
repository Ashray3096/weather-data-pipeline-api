from flask import Blueprint, request
from flask_restx import Api, Resource, fields, reqparse
from models import WeatherData, WeatherStatistics
from extensions import db

# Create a Blueprint for the API
api_bp = Blueprint('api', __name__)

# Create an API instance with documentation available at /docs
api = Api(
    api_bp,
    doc='/docs',
    title='Weather Data API',  # Title for the Swagger documentation
    description='API for managing weather data and statistics',  # Description for the Swagger documentation
    version='1.0.0'  # Version of the API
)

# Define the model for WeatherData to be used in Swagger documentation
weather_data_model = api.model('WeatherData', {
    'id': fields.Integer,
    'station_id': fields.String,
    'date': fields.Date,
    'max_temp': fields.Integer,
    'min_temp': fields.Integer,
    'precipitation': fields.Integer,
})

# Define the model for WeatherStatistics to be used in Swagger documentation
weather_stats_model = api.model('WeatherStatistics', {
    'id': fields.Integer,
    'station_id': fields.String,
    'year': fields.Integer,
    'avg_max_temp': fields.Float,
    'avg_min_temp': fields.Float,
    'total_precipitation': fields.Float,
})

# Define the request parser for weather data queries
weather_parser = reqparse.RequestParser()
weather_parser.add_argument('station_id', type=str, location='args')
weather_parser.add_argument('start_date', type=str, location='args')
weather_parser.add_argument('end_date', type=str, location='args')
weather_parser.add_argument('page', type=int, default=1, location='args')
weather_parser.add_argument('per_page', type=int, default=10, location='args')

class WeatherResource(Resource):
    """
    Resource for handling weather data endpoints.
    """
    @api.expect(weather_parser)
    @api.marshal_with(weather_data_model)
    def get(self):
        """
        Handles GET requests to retrieve weather data.

        Filters data by station_id, start_date, and end_date.
        Supports pagination.
        """
        args = weather_parser.parse_args()
        query = WeatherData.query

        if args['station_id']:
            query = query.filter_by(station_id=args['station_id'])
        if args['start_date']:
            query = query.filter(WeatherData.date >= args['start_date'])
        if args['end_date']:
            query = query.filter(WeatherData.date <= args['end_date'])

        pagination = query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)
        return pagination.items

# Define the request parser for weather statistics queries
stats_parser = reqparse.RequestParser()
stats_parser.add_argument('station_id', type=str, location='args')
stats_parser.add_argument('year', type=int, location='args')
stats_parser.add_argument('page', type=int, default=1, location='args')
stats_parser.add_argument('per_page', type=int, default=10, location='args')

class WeatherStatsResource(Resource):
    """
    Resource for handling weather statistics endpoints.
    """
    @api.expect(stats_parser)
    @api.marshal_with(weather_stats_model)
    def get(self):
        """
        Handles GET requests to retrieve weather statistics.

        Filters data by station_id and year.
        Supports pagination.
        """
        args = stats_parser.parse_args()
        query = WeatherStatistics.query

        if args['station_id']:
            query = query.filter_by(station_id=args['station_id'])
        if args['year']:
            query = query.filter_by(year=args['year'])

        pagination = query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)
        return pagination.items

# Add the resources to the API with their respective endpoints
api.add_resource(WeatherResource, '/weather')
api.add_resource(WeatherStatsResource, '/weather/stats')