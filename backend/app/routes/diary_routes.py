from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Diary, User
from app.models import diary_schema, diary_schemas

diary_routes = Blueprint('diary_routes', __name__)

# This one gets all diaries
@diary_routes.route('/diaries', methods=['GET'])
def get_all_diaries():
    diaries = Diary.query.all()
    return jsonify(diary_schemas.dump(diaries)), 200

# Then this gets a specific diary
@diary_routes.route('/diaries/<int:diary_id>', methods=['GET'])
def get_diary(diary_id):
    diary = Diary.query.get(diary_id)
    return diary_schema.jsonify(diary), 200

# We create a new diary here
@diary_routes.route('/diaries', methods=['POST'])
@jwt_required()
def create_diary():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    data = request.get_json()
    date = data.get('date')
    summary = data.get('summary')
    photo_url = data.get('photo_url')

    new_diary = Diary(date=date, summary=summary, photo_url=photo_url, user_id=user_id)
    db.session.add(new_diary)
    db.session.commit()

    return diary_schema.jsonify(new_diary), 201


# Update diary
@diary_routes.route('/diaries/<int:diary_id>', methods=['PATCH'])
@jwt_required()
def update_diary(diary_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    diary = Diary.query.get(diary_id)

    if diary.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 401

    data = request.get_json()
    date = data.get('date')
    summary = data.get('summary')
    photo_url = data.get('photo_url')

    diary.date = date
    diary.summary = summary
    diary.photo_url = photo_url
    db.session.commit()

    return diary_schema.jsonify(diary), 200

# Delete diary
@diary_routes.route('/diaries/<int:diary_id>', methods=['DELETE'])
@jwt_required()
def delete_diary(diary_id):
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    diary = Diary.query.get(diary_id)

    if diary.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 401

    db.session.delete(diary)
    db.session.commit()

    return jsonify({"msg": "Diary deleted successfully"}), 200