from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Comment, Diary
from app.models import comment_schema, comment_schemas

comment_routes = Blueprint('comment_routes', __name__)

# Here we get all the comments for a specific diary
@comment_routes.route('/diaries/<int:diary_id>/comments', methods=['GET'])
def get_comments_for_diary(diary_id):
    comments = Comment.query.filter_by(diary_id=diary_id).all()
    return jsonify(comment_schemas.dump(comments)), 200

# This section helps to create a new comment for a specific diary
@comment_routes.route('/diaries/<int:diary_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(diary_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    data = request.get_json()
    content = data.get('content')

    new_comment = Comment(content=content, user_id=user_id, diary_id=diary_id)
    db.session.add(new_comment)
    db.session.commit()

    return comment_schema.jsonify(new_comment), 201

