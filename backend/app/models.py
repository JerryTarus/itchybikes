from app import db, ma
from flask_sqlalchemy_serializer import SQLAlchemyAutoSchema
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    diaries = db.relationship('Diary', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='author', lazy=True)
    followers = db.relationship('Follower', back_populates='follower', lazy=True, cascade="all, delete-orphan")
    following = db.relationship('Follower', back_populates='following', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)