from flask import Blueprint

from .user_routes import user_routes
from .diary_routes import diary_routes
from .comment_routes import comment_routes
from .like_routes import like_routes
from .follower_routes import follower_routes
from .auth_routes import auth_routes  

# Register the blueprints
def register_routes(app):
    app.register_blueprint(user_routes)
    app.register_blueprint(diary_routes)
    app.register_blueprint(comment_routes)
    app.register_blueprint(like_routes)
    app.register_blueprint(follower_routes)
    app.register_blueprint(auth_routes)  # This registers auth routes

# Function to initialize all routes
def init_app(app):
    # This import is for routes responsible for initialization
    from . import user_routes, diary_routes, comment_routes, like_routes, follower_routes, auth_routes

    # Here we call the register function for each route module
    register_routes(app)
