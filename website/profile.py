from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from .db_config import db
import json
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from website.form import UpdateAccountForm

import secrets
import os
from PIL import Image
from website.views import app

profile = Blueprint('profile', __name__)

# Save_picture code taken from: https://youtu.be/803Ei2Sq-Zs
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/assets/profile_pictures', picture_fn)
    output_size = (400,400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@profile.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def viewProfile(user_id):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
            db.session.commit()
            flash('Image Uploaded!', category='success')
        else:
            flash('Please upload an image!', category='error')
        return redirect("/profile/" + str(user_id))
    user = User.query.filter_by(id=user_id).first()
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.date.desc()).limit(3).all()
        # INNER JOIN User ON Note.user_id == User.id AND user_id == user.id ORDER BY Note.date DESC LIMIT 4
    image_file = url_for('static', filename='assets/profile_pictures/' + user.profile_picture)
    return render_template("profile.html", notes=notes, user=user, image_file=image_file, form=form)


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