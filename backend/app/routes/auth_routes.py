from app import db
from flask import make_response

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from app.models import User



auth_routes = Blueprint('auth_routes', __name__)
auth_bp = Blueprint('auth', __name__)

CORS(auth_routes)

# json encoder
# app.json_encoder = json.JSONEncoder

@auth_routes.route('/hello')
def hello():
    return 'Welcome to Itchy Bikes'



@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Received login request with data:", data)
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    else:
        print("Login failed for user:", data['email'])
        return jsonify({"msg": "Oups!!! Invalid credentials"}), 401
    

@auth_routes.route('/login', methods=['OPTIONS'])
def login_options():
    
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response




@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Check if user with the provided email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"msg": "Email is already registered"}), 400
    
    # Create a new user
    new_user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password']))
    
    # Add new user to the db
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Signup successful"}), 201
    


@auth_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
