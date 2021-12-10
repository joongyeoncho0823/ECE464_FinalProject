from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


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
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True)
    discussion_id = db.Column(
        db.Integer, db.ForeignKey('discussion.id', ondelete='CASCADE'))


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
