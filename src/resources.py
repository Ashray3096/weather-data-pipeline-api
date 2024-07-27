from flask import Blueprint, request
from flask_restx import Api, Resource, fields, reqparse
from models import WeatherData, WeatherStatistics
from extensions import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp, doc='/docs')

weather_data_model = api.model('WeatherData', {
    'id': fields.Integer,
    'station_id': fields.String,
    'date': fields.Date,
    'max_temp': fields.Integer,
    'min_temp': fields.Integer,
    'precipitation': fields.Integer,
})

weather_stats_model = api.model('WeatherStatistics', {
    'id': fields.Integer,
    'station_id': fields.String,
    'year': fields.Integer,
    'avg_max_temp': fields.Float,
    'avg_min_temp': fields.Float,
    'total_precipitation': fields.Float,
})

weather_parser = reqparse.RequestParser()
weather_parser.add_argument('station_id', type=str, location='args')
weather_parser.add_argument('start_date', type=str, location='args')
weather_parser.add_argument('end_date', type=str, location='args')
weather_parser.add_argument('page', type=int, default=1, location='args')
weather_parser.add_argument('per_page', type=int, default=10, location='args')

class WeatherResource(Resource):
    @api.expect(weather_parser)
    @api.marshal_with(weather_data_model)
    def get(self):
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

stats_parser = reqparse.RequestParser()
stats_parser.add_argument('station_id', type=str, location='args')
stats_parser.add_argument('year', type=int, location='args')
stats_parser.add_argument('page', type=int, default=1, location='args')
stats_parser.add_argument('per_page', type=int, default=10, location='args')

class WeatherStatsResource(Resource):
    @api.expect(stats_parser)
    @api.marshal_with(weather_stats_model)
    def get(self):
        args = stats_parser.parse_args()
        query = WeatherStatistics.query

        if args['station_id']:
            query = query.filter_by(station_id=args['station_id'])
        if args['year']:
            query = query.filter_by(year=args['year'])

        pagination = query.paginate(page=args['page'], per_page=args['per_page'], error_out=False)
        return pagination.items

api.add_resource(WeatherResource, '/weather')
api.add_resource(WeatherStatsResource, '/weather/stats')