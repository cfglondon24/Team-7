from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy.orm import relationship


class RoleEnum(Enum):
    SUPPORTER = 'supporter'
    PATIENT = 'patient'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # Max Length 150
    password = db.Column(db.String(150))
    role = db.Column(db.Enum(RoleEnum))
    first_name = db.Column(db.String(150))
    location = db.Column(db.String(150))
    diaries = db.relationship('Diary')
    posts = db.relationship('Post')

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    caption = db.Column(db.String(500))
    comments = db.relationship('Comment')
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())