from flask import Blueprint, request, jsonify
from os import getenv as env
from datetime import datetime
import googlemaps

gmaps = googlemaps.Client(key=env("MAPS_KEY"))

maps_api_routes = Blueprint('maps_api_routes', __name__)

@maps_api_routes.route('/directions', methods=['POST'])
async def directions():
    if request.method != 'POST':
        return jsonify({"error": "Invalid request method"}), 405
    
    date = datetime.now()

    data = request.get_json()
    
    origin = data.get("origin")
    destination = data.get("destination")
    #transit, driving, walking, bicycling
    mode = data.get("mode")

    if not origin or not destination:
        return jsonify({"error": "Invalid request parameters"}), 400
    
    directions_result = gmaps.directions(origin,
                                        destination,
                                        mode,
                                        language='pt_BR',
                                        departure_time=date)
    
    steps = directions_result[0].get("legs")[0].get("steps")
    num_count = 0
    num_list = []
    for step in steps:
        distancia = step.get("distance").get("text").split(" ")
        if distancia[1] == "km":
            distancia[0] = float(distancia[0].replace(",", ".")) * 1000
        distancia[0] = int(distancia[0])     

        duracao = step.get("duration").get("text").split(" ")
        duracao[0] = int(duracao[0]) * 60
        
        num_list.append(int(distancia[0] / duracao[0]))
        num_count+= distancia[0] / duracao[0]

    num_media = int(num_count / len(steps))
    print(num_list)
    return jsonify(directions_result), 200
 
@maps_api_routes.route("/geocode", methods=['POST'])
async def geocode():
    data = request.get_json()
    address = data.get("address")
    
    if not address:
        return jsonify({"error": "Invalid request parameters"}), 400
    
    geocode_result = gmaps.geocode(address)
    
    return jsonify(geocode_result), 200