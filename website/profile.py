from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from .db_config import db
import json

profile = Blueprint('profile', __name__)


@profile.route('/profile/<int:user_id>')
def viewProfile(user_id):
    user = User.query.filter_by(id=user_id).first()
    notes = Note.query.filter_by(
        user_id=user_id).order_by(Note.date.desc()).limit(3).all()
    # INNER JOIN User ON Note.user_id == User.id AND user_id == user.id ORDER BY Note.date DESC LIMIT 4
    return render_template("profile.html", notes=notes, user=user)


# @profile.route('/profile')
# def viewProfile():
#     return render_template("profile.html", user=current_user)

@profile.route('/updateProfile')
def updateProfile():
    return render_template("updateInfo.html", user=current_user)
