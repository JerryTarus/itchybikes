from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy_serializer import FlaskSQLAlchemySerializer


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
api = Api()
serializer = FlaskSQLAlchemySerializer()

