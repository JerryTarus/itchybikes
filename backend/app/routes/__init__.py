from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# SQLAlchemy and JWT instances
db = SQLAlchemy()
jwt = JWTManager()

# Blueprints definitions
user_bp = Blueprint('user_routes', __name__)
auth_bp = Blueprint('auth_routes', __name__)

# Import the routes
from .auth_routes import auth_routes
from .user_routes import user_routes
from .diary_routes import diary_routes
from .comment_routes import comment_routes
from .like_routes import like_routes
from .follower_routes import follower_routes

# Function to create the Flask app
def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.Config')

    # Initialise the extensions
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(diary_routes, url_prefix='/api')
    app.register_blueprint(comment_routes, url_prefix='/api')
    app.register_blueprint(like_routes, url_prefix='/api')
    app.register_blueprint(follower_routes, url_prefix='/api')

    print("Registered Blueprints:")
    print(app.url_map)

    return app

from .auth_routes import *
from .user_routes import *
from .diary_routes import *
from .comment_routes import *
from .like_routes import *
from .follower_routes import *
