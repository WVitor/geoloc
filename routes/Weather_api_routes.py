from flask import Blueprint, request, jsonify
from services.Weather_api import Weather_api
weather_api_routes = Blueprint('weather_api_routes', __name__)

@weather_api_routes.route("/current", methods=['POST'])
async def current():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_current(city))

@weather_api_routes.route("/forecast", methods=['POST'])
async def forecast():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_forecast(city))

@weather_api_routes.route("/search", methods=['POST'])
async def search():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_search(city))

@weather_api_routes.route("/history", methods=['POST'])
async def history():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_history(city))

@weather_api_routes.route("/future", methods=['POST'])
async def future():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_future(city))

@weather_api_routes.route("/astronomy", methods=['POST'])
async def astronomy():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_astronomy(city))

@weather_api_routes.route("/time-zone", methods=['POST'])
async def time_zone():
    data = request.get_json()
    city = data.get("city")
    weather_api = Weather_api()
    return jsonify(weather_api.get_time_zone(city))
