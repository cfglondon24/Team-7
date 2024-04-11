from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Post, Comment, User, Diary, RoleEnum

views = Blueprint('views', __name__)

# Define the home URL route
@views.route('/', methods=['GET', 'POST']) #decorator
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/social-media', methods=['GET', 'POST'])
@login_required
def social_media():
    if request.method == 'POST':
        if 'postButton' in request.form:
            caption = request.form.get('caption')
            print(caption)
            new_post = Post(caption=caption, user=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.social_media'))

    posts = Post.query.all()
    captions = Post.query.with_entities(Post.caption).all()
    print(captions)
    return render_template("socialMedia.html", user=current_user, posts=posts)

@views.route('/calendar', methods=['GET', 'POST'])
@login_required
def event():
    return render_template("eventSignUp.html", user=current_user)

@views.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    if request.method == 'POST':
        print(request.form.get('diary'))
        new_diary = Diary(
            happiness_level=request.form.get('happiness_level'), 
            exercise_minutes = request.form.get('exercise_minutes'),
            explanation = request.form.get('explanation'),
            user=current_user.id)
        db.session.add(new_diary)
        db.session.commit()
        flash('diary added!', category='success')

    return render_template("diary.html", user=current_user)