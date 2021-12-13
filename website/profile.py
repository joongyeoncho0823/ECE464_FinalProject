from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Post, User
from .db_config import db
import json

profile = Blueprint('profile', __name__)


@profile.route('/profile/<int:user_id>')
def viewProfile(user_id):
    user = User.query.filter_by(id=user_id).first()
    posts = db.session.execute(
        "SELECT * FROM Post INNER JOIN User ON Post.user_id == User.id AND user_id == user.id ORDER BY Post.date DESC LIMIT 4")
    return render_template("profile.html", posts=posts, user=user)


# @profile.route('/profile')
# def viewProfile():
#     return render_template("profile.html", user=current_user)

@profile.route('/updateProfile')
def updateProfile():
    return render_template("updateInfo.html", user=current_user)
