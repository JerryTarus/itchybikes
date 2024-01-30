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
    

class Diary(db.Model):
    diary_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    comments = db.relationship('Comment', backref='diary', lazy=True)
    likes = db.relationship('Like', backref='diary', lazy=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    diary_id = db.Column(db.Integer, db.ForeignKey('diary.diary_id'), nullable=False)

class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    diary_id = db.Column(db.Integer, db.ForeignKey('diary.diary_id'), nullable=False)

class Follower(db.Model):
    follower_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    follower_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    following_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    follower = db.relationship('User', foreign_keys=[follower_user_id], back_populates='followers')
    following = db.relationship('User', foreign_keys=[following_user_id], back_populates='following')