from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Follower, User
from app.models import follower_schema, follower_schemas

follower_routes = Blueprint('follower_routes', __name__)


# Get all followers for a specific user
@follower_routes.route('/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    followers = Follower.query.filter_by(following_user_id=user_id).all()
    return jsonify(follower_schemas.dump(followers)), 200

# Follow a user
@follower_routes.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user = get_jwt_identity()
    follower_user_id = current_user['user_id']

    new_follower = Follower(follower_user_id=follower_user_id, following_user_id=user_id)
    db.session.add(new_follower)
    db.session.commit()

    return follower_schema.jsonify(new_follower), 201

# Unfollow a user
@follower_routes.route('/users/<int:user_id>/unfollow', methods=['DELETE'])
@jwt_required()
def unfollow_user(user_id):
    current_user = get_jwt_identity()
    follower_user_id = current_user['user_id']

    follower = Follower.query.filter_by(follower_user_id=follower_user_id, following_user_id=user_id).first()

    if not follower:
        return jsonify({"msg": "You are not following this user"}), 404

    db.session.delete(follower)
    db.session.commit()

    return jsonify({"msg": "Unfollowed successfully"}), 200