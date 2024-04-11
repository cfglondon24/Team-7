from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import ImageColumn


class RoleEnum(Enum):
    SUPPORTER = 'supporter'
    PATIENT = 'patient'

# user_community = Table('user_community',
#                        db.Model.metadata,
#                        Column('user_id', Integer, ForeignKey('user.id')),
#                        Column('community_id', Integer, ForeignKey('community.id'))
#                        )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # Max Length 150
    password = db.Column(db.String(150))
    role = db.Column(db.Enum(RoleEnum))
    first_name = db.Column(db.String(150))
    location = db.Column(db.String(150))
    diaries = db.relationship('Diary')
    posts = db.relationship('Post')
    # communities = db.relationship('Community')
    # communities = db.relationship('Community', secondary=user_community, backref='users')


class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    caption = db.Column(db.String(500))
    # photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)), nullable=True)
    comments = db.relationship('Comment')
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey('post.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


# class Community(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150))
#     # users = db.relationship('User')
#     users = db.relationship('User', secondary=user_community, backref='communities')