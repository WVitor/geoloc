from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager
import requests as req
from datetime import timedelta
from os import getenv as env
from services.Maps_api import Maps_api
from flask_cors import CORS
#from flask_session import Session
import googlemaps
from dao.feedbackDao import inserir_feedback, alterar_tabela_feedback
from model.feedback import Feedback
import json

from routes.Weather_api_routes import weather_api_routes
from routes.Maps_api_routes import maps_api_routes
from routes.Autentication_routes import autentication_routes

gmaps = googlemaps.Client(key=env("MAPS_KEY"))

app = Flask(__name__, template_folder='views', static_folder='static')


### CORS CONFIG ###
CORS(app, resources={r"/*": {"origins": "*"}})

### JWT CONFIG ###
app.config['JWT_SECRET_KEY'] = env("JWT_SECRET")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)

### Autentication CONFIG ###
app.register_blueprint(autentication_routes, url_prefix='/auth')

### MAPS API
app.register_blueprint(maps_api_routes, url_prefix='/maps')

### WEATHER API
app.register_blueprint(weather_api_routes, url_prefix='/weather')

### ROUTES DEFAULT
@app.route("/contato", methods=['GET'])
async def contato():
    return render_template('pages/contato.html', title='Contato')


@app.route("/feedback", methods=["POST"])
async def feedback():
    if request.method == 'POST' :
        try:
            data = json.loads(request.get_data())
            feed = data.get("feed")
            msg = data.get("msg")

            if feed != True and feed != False:
                return jsonify({"error": "Invalid request parameters"}), 400
            
            feedback = Feedback()
            feedback.set_feed(feed)
       
            if feed == False and msg:
                feedback.set_msg(msg)

            inserir_feedback(feedback)
            return jsonify({"success": "Feedback enviado com sucesso.", "status": 200})
        except:
            return jsonify({"error": "Não foi possivel enviar o feedback.", "status": 500})

@app.route("/places-old", methods=['GET', "POST"])
async def places_old():
    lugares = []
    if request.method == 'POST':
        lugares.clear()
        location_address = request.form.get("location")
        location_place = request.form.get("place")
        radius = 3000

        if not location_address or not location_place:
            return render_template('pages/places.html', title='Lugares', lugares=lugares, error="Informe um endereço valido.")
        
        try:
            location_result = gmaps.geocode(location_address)[0].get("geometry").get("location")
        except:
            return render_template('pages/places.html', title='Lugares', lugares=lugares, error="Informe um endereço valido.")

        location_lat_lng = f"{location_result.get('lat')},{location_result.get('lng')}"
        maps_api = Maps_api()
        
        brute_places = maps_api.get_places(location_lat_lng, location_place, radius)

        if not brute_places.get("results"):
            return render_template('pages/places.html', title='Lugares', lugares=lugares, error= "Não foi possivel localizar lugares abertos proximos a esta localização.")
        
        for place in brute_places.get("results"):
            if place.get("opening_hours") and place.get("opening_hours").get("open_now"):
                if(place.get("photos") != None):
                    photo_reference = place.get("photos")[0].get("photo_reference")
                    photo = req.get(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_reference}&key={env('MAPS_KEY')}")
                    lugares.append({
                        "key": place.get("place_id"),
                        "name": place.get("name"),
                        "address": place.get("vicinity"),
                        "rating": place.get("rating"),
                        "types": place.get("types"),
                        "location": place.get("geometry").get("location"),
                        "status": 'Aberto',
                        "photo": photo.url
                    })
                else:
                    lugares.append({
                        "key": place.get("place_id"),
                        "name": place.get("name"),
                        "address": place.get("vicinity"),
                        "rating": place.get("rating"),
                        "types": place.get("types"),
                        "location": place.get("geometry").get("location"),
                        "status": 'Aberto',
                        "photo": "https://static.thenounproject.com/png/3083030-200.png"
                    })
        
        return render_template('pages/places.html', title='Lugares', lugares=lugares)
        #return redirect(url_for('places', lugares=lugares))
    elif request.method == 'GET':
        return render_template('pages/places.html', title='Lugares', lugares=lugares)
    
@app.route("/places", methods=['GET', "POST"])
async def places():
    lugares = []
    if request.method == 'POST':
        lugares.clear()
        data = json.loads(request.get_data())
        location_address = data.get("location")
        location_place = data.get("place")
        radius = 3000

        if not location_address or not location_place:
            return render_template('pages/places.html', title='Lugares', lugares=lugares, error="Informe um endereço valido.")
        
        try:
            location_result = gmaps.geocode(location_address)[0].get("geometry").get("location")
        except:
            return render_template('pages/places.html', title='Lugares', lugares=lugares, error="Informe um endereço valido.")

        location_lat_lng = f"{location_result.get('lat')},{location_result.get('lng')}"
        maps_api = Maps_api()
        
        brute_places = maps_api.get_places(location_lat_lng, location_place, radius)

        if not brute_places.get("results"):
            return render_template('pages/places.html', title='Lugares', lugares=lugares, error= "Não foi possivel localizar lugares abertos proximos a esta localização.")
        
        for place in brute_places.get("results"):
            if place.get("opening_hours") and place.get("opening_hours").get("open_now"):
                if(place.get("photos") != None):
                    photo_reference = place.get("photos")[0].get("photo_reference")
                    photo = req.get(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_reference}&key={env('MAPS_KEY')}")
                    lugares.append({
                        "key": place.get("place_id"),
                        "name": place.get("name"),
                        "address": place.get("vicinity"),
                        "rating": place.get("rating"),
                        "types": place.get("types"),
                        "location": place.get("geometry").get("location"),
                        "status": 'Aberto',
                        "photo": photo.url
                    })
                else:
                    lugares.append({
                        "key": place.get("place_id"),
                        "name": place.get("name"),
                        "address": place.get("vicinity"),
                        "rating": place.get("rating"),
                        "types": place.get("types"),
                        "location": place.get("geometry").get("location"),
                        "status": 'Aberto',
                        "photo": "https://static.thenounproject.com/png/3083030-200.png"
                    })
        
        return render_template('pages/places.html', title='Lugares', lugares=lugares)
        #return redirect(url_for('places', lugares=lugares))
    elif request.method == 'GET':
        return render_template('pages/places.html', title='Lugares', lugares=lugares)

@app.route("/get_places", methods=['POST'])
async def get_places():
    if request.method == 'POST':
        lugares = {}
        data = json.loads(request.get_data())
        location_address = data.get("location")
        location_place = data.get("place")
        radius = 3000

        if not location_address or not location_place:
            return jsonify({"error": "Informe um endereço valido."}), 400
        
        try:
            location_result = gmaps.geocode(location_address)[0].get("geometry").get("location")
            lugares.update({"location": location_result})
        except:
            return jsonify({"error":"Informe um endereço valido."}), 400

        location_lat_lng = f"{location_result.get('lat')},{location_result.get('lng')}"
        
        maps_api = Maps_api()
        
        brute_places = maps_api.get_places(location_lat_lng, location_place, radius)

        if not brute_places.get("results"):
            return jsonify({"error":"Não foi possivel localizar lugares abertos proximos a esta localização."}), 400
        
        lugares.update({"result": []})
        for place in brute_places.get("results"):
            photo = req.get(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={place.get('photos')[0].get('photo_reference')}&key={env('MAPS_KEY')}") if place.get("photos") != None else None
            lugares.get("result").append({
                "title": place.get("name"),
                "location": place.get("geometry").get("location"),
                "content": {
                    "status": 'Aberto' if place.get("opening_hours") and place.get("opening_hours").get("open_now") else 'Fechado',
                    "photo": photo.url if photo != None else "https://static.thenounproject.com/png/3083030-200.png",
                    "address": place.get("vicinity"),
                    "rating": place.get("rating"),
                    "types": place.get("types")
                }
        })
        
        return jsonify(lugares), 200

@app.route("/rotas", methods=['GET', "POST"])
async def rotas():
    if request.method == 'GET':
        return render_template('pages/rotas.html', title='Rotas', maps_key=env("MAPS_KEY"))

@app.route('/', methods=['GET'])
async def index():
    return redirect(url_for('places', lugares=[]))

if __name__ == '__main__':
    app.run(debug=True)

#produção linux
#gunincorn --bind 0.0.0.0:5000 main:app
#gunicorn main:app 

#producao windows
#waitress-serve --listen=*:5000 main:app

#pip freeze -> requirements.txt