from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import *


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='author', lazy=True)
    discussions = db.relationship(
        'Discussion', secondary='UserDiscussion')


class UserDiscussion(db.Model):
    __tablename__ = 'UserDiscussion'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    discussion_id = db.Column(
        db.Integer, db.ForeignKey('discussion.id', ondelete='CASCADE'))


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    participants = db.relationship('User', secondary='UserDiscussion')
    # posts = db.relationship('Note', backref='group', lazy=True)
    # password = db.Column(db.String(150))
