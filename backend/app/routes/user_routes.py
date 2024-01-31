from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Diary, Follower
from app.models import user_schema, user_schemas

user_routes = Blueprint('user_routes', __name__)

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile')
def profile():
    return 'User Profile!'

# Get all users
@user_routes.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify(user_schemas.dump(users)), 200

# Get a specific user's profile
@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    return user_schema.jsonify(user), 200

# Update the user's profile
@user_routes.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user_profile(user_id):
    current_user = get_jwt_identity()
    if current_user['user_id'] != user_id:
        return jsonify({"msg": "Unauthorized"}), 401

    user = User.query.get(user_id)
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.set_password(data.get('password', user.password))

    db.session.commit()

    return user_schema.jsonify(user), 200

# DANGER ZONE
# Delete the user's account
@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_account(user_id):
    current_user = get_jwt_identity()
    if current_user['user_id'] != user_id:
        return jsonify({"msg": "Unauthorized"}), 401

    user = User.query.get(user_id)

    # Delete user's diaries, comments, likes, and followers
    for diary in user.diaries:
        db.session.delete(diary)

    for comment in user.comments:
        db.session.delete(comment)

    for like in user.likes:
        db.session.delete(like)

    for follower in user.followers:
        db.session.delete(follower)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "Account deleted successfully"}), 200
