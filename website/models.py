from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import *


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    discussions = db.relationship(
        'Discussion', secondary='UserDiscussion', backref=db.backref('participants', lazy='dynamic'))


class UserDiscussion(db.Model):
    __tablename__ = 'UserDiscussion'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    discussion_id = db.Column(
        db.Integer, db.ForeignKey('discussion.id', ondelete='CASCADE'))


# user_discussion = db.Table('user_discussion', db.Model.metadata, db.Column('user_id', db.Integer, db.ForeignKey(
#     'user.id')), db.Column('discussion_id', db.Integer, db.ForeignKey('discussion.id')))


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
