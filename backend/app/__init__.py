from flask import Flask, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
api = Api()
jwt = JWTManager()
serializer = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Check if the 'FLASK_ENV' variable is set
    flask_env = os.environ.get('FLASK_ENV')

    if flask_env == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif flask_env == 'production':
        app.config.from_object('config.ProductionConfig')

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    api.init_app(app)
    serializer.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register blueprints here
    from app.routes.user_routes import user_routes
    from app.routes.diary_routes import diary_routes
    from app.routes.comment_routes import comment_routes
    from app.routes.like_routes import like_routes
    from app.routes.follower_routes import follower_routes
    from app.routes.auth_routes import auth_routes

    app.register_blueprint(user_routes)
    app.register_blueprint(diary_routes)
    app.register_blueprint(comment_routes)
    app.register_blueprint(like_routes)
    app.register_blueprint(follower_routes)
    app.register_blueprint(auth_routes)

    # Serve images during development
    if flask_env == 'development':
        @app.route('/images/<path:filename>')
        def serve_image(filename):
            return send_from_directory(os.path.join(app.root_path, 'images'), filename)

    return app
