from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from .models import Note, Discussion, User
from .db_config import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    posts = db.session.execute(
        "SELECT DISTINCT * FROM Note, User, user_discussion, Discussion WHERE user_discussion.user_id == Note.user_id AND Note.discussion_id == Discussion.id AND user_discussion.user_id == User.id AND Note.discussion_id == user_discussion.discussion_id ORDER BY Note.date DESC")

    return render_template("home.html", posts=posts,  user=current_user)

# @views.route('/home_post_sorted/<int:sort>/<int:order>', methods=['GET', 'POST'])
# @login_required
# def home_post_sorted(sort, order):

#     return render_template("discussions.html", user=current_user)


@ views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@ views.route('/add', methods=['GET', 'POST'])
@ login_required
def add():
    if request.method == 'POST':
        note = request.form.get('note')
        title = request.form.get('title')
        discussion = request.form.get('discussion_select')
        if len(note) < 1:
            flash('Post is too short!', category='error')
        else:
            discussion_choice = Discussion.query.filter_by(
                discussion_name=discussion).first()  # groups should be able to have the same name..
            new_note = Note(title=title, data=note,
                            user_id=current_user.id)
            discussion_choice.posts.append(new_note)
            db.session.add(new_note)
            db.session.commit()
            flash('Posted!', category='success')
            return redirect(url_for('views.home'))
    my_discussions = current_user.discussions.all()
    return render_template("addPost.html", my_discussions=my_discussions, user=current_user)


@ views.route('/discussion_page')
@ login_required
def discussion_page():
    user = current_user

    return render_template("discussions.html", user=current_user)


@ views.route('/discussion/<int:discussion_id>')
@ login_required
def discussion(discussion_id):
    discussion = Discussion.query.filter_by(id=discussion_id).first()
    posts = Note.query.filter_by(
        discussion_id=discussion_id).order_by(Note.date.desc())

    return render_template("discussion.html", posts=posts, discussion=discussion, user=current_user)


@ views.route('/addGroup', methods=['GET', 'POST'])
@ login_required
def addGroup():
    if request.method == 'POST':  # if it is add
        name = request.form.get('groupName')
        newGroup = Discussion(discussion_name=name)
        user = current_user
        user.discussions.append(newGroup)
        db.session.add(newGroup)
        db.session.commit()
        flash('Group Created!', category='success')
        return redirect(url_for('views.home'))
    discussions = Discussion.query.all()
    return render_template("join.html", discussions=discussions, user=current_user)


@ views.route('/joinGroup', methods=['POST'])
@ login_required
def joinGroup():
    if request.method == 'POST':  # if it is add
        group_name = request.form.get('discussion_join')
        group = Discussion.query.filter_by(discussion_name=group_name).first()
        user = current_user
        try:
            user.discussions.append(group)
            db.session.commit()
            flash('Group joined!', category='success')
            return redirect(url_for('views.home'))
        except IntegrityError:
            db.session.rollback()
            flash('You are already a member of this group!', category='error')
            return redirect(url_for('views.home'))
    discussions = Discussion.query.all()
    return render_template("join.html", discussions=discussions, user=current_user)


@ views.route('/leaveGroup/<int:discussion_id>', methods=['GET', 'POST'])
@ login_required
def leaveGroup(discussion_id):
    discussion = Discussion.query.filter_by(id=discussion_id).first()
    user = current_user
    flash('Left group', category='success')
    user.discussions.remove(discussion)
    db.session.commit()
    return redirect(url_for('views.home'))
