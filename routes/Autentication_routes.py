from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token

autentication_routes = Blueprint('autentication_routes', __name__)

@autentication_routes.route('/login', methods=['POST'])
async def login():
    data = request.get_json()
    
    username = data.get("username")
    password = data.get("password")
    
    if username != "admin" and password != "admin":
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = create_access_token(identity=username)
    
    return jsonify({"token": token}), 200

@autentication_routes.route('/protegido', methods=['GET'])
@jwt_required()
async def protegido():
    return jsonify({"message": "Acceso permitido"}), 200    
