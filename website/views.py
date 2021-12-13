from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from .models import Post, Discussion, User
from .db_config import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    # posts = db.session.execute(
    #     "SELECT DISTINCT U.user_id, U.discussion_id FROM user_discussion U, Post N JOIN (SELECT * FROM Post N) ON N.discussion_id == U.discussion_id")
    # posts = db.session.execute(
    #     "SELECT DISTINCT Post.title, Post.data, Post.date, user_discussion.user_id, user_discussion.discussion_id, Discussion.name as discussion_name FROM Post JOIN user_discussion JOIN Discussion WHERE Post.discussion_id == user_discussion.discussion_id AND user_discussion.discussion_id == Discussion.id")
    # posts = db.session.execute(
    #     "SELECT DISTINCT * FROM (Post LEFT OUTER JOIN user_discussion) JOIN Discussion JOIN USER WHERE Post.discussion_id == user_discussion.discussion_id AND user_discussion.discussion_id == Discussion.id AND User.id == Post.user_id ORDER BY Post.date DESC")
    posts = db.session.execute(
        "SELECT DISTINCT * FROM user_discussion,User,Post WHERE User.id == Post.user_id AND user_discussion.user_id == User.id AND user_discussion.discussion_id == Post.discussion_id AND true ORDER BY Post.date DESC")
    # posts = db.session.execute(
    #     "SELECT DISTINCT * FROM Discussion, user_discussion,User WHERE user_disccusion.discussion_id == Discussion.id AND User.id == user_discussion.user_id")
    this_discussion = Discussion.query.filter_by(id=1).first()
    # posts = db.session.query(
    #     Post.author, Post.id, Post.data).filter(Post.id == 1).first()
    #

    # db.session.execute(
    #     "SELECT * FROM Post INNER JOIN User ON Post.user_id == User.id AND user_id == user.id ORDER BY Post.date DESC LIMIT 4")
    # posts = Post.query.filter()
    return render_template("home.html", posts=posts, this_discussion=this_discussion, user=current_user)

# @views.route('/home_post_sorted/<int:sort>/<int:order>', methods=['GET', 'POST'])
# @login_required
# def home_post_sorted(sort, order):

#     return render_template("discussions.html", user=current_user)


@ views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})


@ views.route('/add', methods=['GET', 'POST'])
@ login_required
def add():
    if request.method == 'POST':
        post = request.form.get('post')
        title = request.form.get('title')
        discussion = request.form.get('discussion_select')
        if len(post) < 1:
            flash('Post is too short!', category='error')
        else:
            discussion_choice = Discussion.query.filter_by(
                name=discussion).first()  # groups should be able to have the same name..
            new_post = Post(title=title, data=post,
                            user_id=current_user.id)
            discussion_choice.posts.append(new_post)
            db.session.add(new_post)
            db.session.commit()
            flash('Posted!', category='success')
            return redirect(url_for('views.home'))

    return render_template("addPost.html", user=current_user)


@ views.route('/discussion_page')
@ login_required
def discussion_page():
    user = current_user

    return render_template("discussions.html", user=current_user)


@ views.route('/discussion/<int:discussion_id>')
@ login_required
def discussion(discussion_id):
    discussion = Discussion.query.filter_by(id=discussion_id).first()

    return render_template("discussion.html", discussion=discussion, user=current_user)


@ views.route('/addGroup', methods=['GET', 'POST'])
@ login_required
def addGroup():
    if request.method == 'POST':  # if it is add
        name = request.form.get('groupName')
        newGroup = Discussion(name=name)
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
        group = Discussion.query.filter_by(name=group_name).first()
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
