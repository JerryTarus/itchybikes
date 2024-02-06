from app import create_app, db
from flask_cors import CORS
from flask import Flask, json


app = create_app()
CORS(app)
# app.json_encoder = json.JSONEncoder
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
