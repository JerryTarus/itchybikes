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

