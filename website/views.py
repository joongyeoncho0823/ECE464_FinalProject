from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Discussion
from .db_config import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Posted!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        note = request.form.get('note')
        title = request.form.get('title')
        # title = request.form.get('title')
        if len(note) < 1:
            flash('Post is too short!', category='error')
        else:
            new_note = Note(title=title, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Posted!', category='success')
            return redirect(url_for('views.home'))

    return render_template("addPost.html", user=current_user)


@views.route('/discussion_page')
@login_required
def discussion_page():
    return render_template("discussions.html", user=current_user)


@views.route('/addGroup', methods=['GET', 'POST'])
@login_required
def addGroup():
    if request.method == 'POST':
        name = request.form.get('groupName')
        newGroup = Discussion(name=name)
        user = current_user
        user.discussions.append(newGroup)
        db.session.add(newGroup)
        db.session.commit()
        flash('Group Created!', category='success')
        return redirect(url_for('views.home'))

    return render_template("join.html", user=current_user)
