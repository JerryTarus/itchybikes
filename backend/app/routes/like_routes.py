from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Like, Diary
from app.models import like_schema, like_schemas

like_routes = Blueprint('like_routes', __name__)

# Get all likes for a specific diary
@like_routes.route('/diaries/<int:diary_id>/likes', methods=['GET'])
def get_likes_for_diary(diary_id):
    likes = Like.query.filter_by(diary_id=diary_id).all()
    return jsonify(like_schemas.dump(likes)), 200

# Like a diary
@like_routes.route('/diaries/<int:diary_id>/like', methods=['POST'])
@jwt_required()
def like_diary(diary_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    like = Like.query.filter_by(user_id=user_id, diary_id=diary_id).first()

    if like:
        return jsonify({"msg": "You already liked this diary"}), 400

    new_like = Like(user_id=user_id, diary_id=diary_id)
    db.session.add(new_like)
    db.session.commit()

    return like_schema.jsonify(new_like), 201

# Unlike a diary
@like_routes.route('/diaries/<int:diary_id>/unlike', methods=['DELETE'])
@jwt_required()
def unlike_diary(diary_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    like = Like.query.filter_by(user_id=user_id, diary_id=diary_id).first()

    if not like:
        return jsonify({"msg": "Unliked diary"}), 404

    db.session.delete(like)
    db.session.commit()

    return jsonify({"msg": "Unliked diary"}), 200