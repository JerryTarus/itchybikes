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