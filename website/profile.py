from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from .db_config import db
import json
from werkzeug.security import generate_password_hash

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

@profile.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')

        bValid = True
        
        if email:

            if len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
                bValid = False
            else:
                current_user.email = email
        if first_name:
            if len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
                bValid = False
            else:
                current_user.first_name = first_name 
        if password1:
            if len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
                bValid = False
            else:
                current_user.password = generate_password_hash(password1, method='sha256') 

        try:
            assert(bValid)
            db.session.commit()
            flash('Account Updated!', category='success')
            return redirect(url_for('views.home'))
        except:
            db.session.rollback()
            if bValid:
                flash('Email already exists.', category='error')
        
    return render_template("updateInfo.html", user=current_user)