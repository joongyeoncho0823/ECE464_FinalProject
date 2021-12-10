from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

profile = Blueprint('profile', __name__)


@profile.route('/profile')
def viewProfile():
    return render_template("profile.html", user=current_user)
