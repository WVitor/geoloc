from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from flask_jwt_extended import JWTManager

from datetime import timedelta
from os import getenv as env

from routes.Weather_api_routes import weather_api_routes
from routes.Maps_api_routes import maps_api_routes
from routes.Autentication_routes import autentication_routes

app = Flask(__name__, template_folder='views', static_folder='static')

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

@app.route('/', methods=['GET'])
async def index():
    return render_template('pages/home.html', title='Home')

if __name__ == '__main__':
    app.run(debug=True)

#produção linux
#gunincorn --bind 0.0.0.0:5000 main:app
#gunicorn main:app 

#producao windows
#waitress-serve --listen=127.0.0.1:5000 main:app