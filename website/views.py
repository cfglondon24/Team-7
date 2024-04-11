from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Post, Comment, User, Diary, RoleEnum

views = Blueprint('views', __name__)

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

@views.route('/calendar', methods=['GET', 'POST']) #decorator
#@login_required
def calendar():
    # Sample event data
    events = [
        {
            'title': 'Event 1',
            'start': '2024-04-11'
        },
        {
            'title': 'Event 2',
            'start': '2024-04-15'
        }
    ]
    return render_template("calendar.html", user=current_user, events=events)

# Define the home URL route
@views.route('/', methods=['GET', 'POST']) #decorator
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

from random import choice

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

    # Check if there are less than 10 posts with captions about mental health
    mental_health_captions = [
        "It's okay not to be okay sometimes. #mentalhealthawareness",
        "Let's break the stigma surrounding mental health. #endthestigma",
        "Taking care of your mental health is just as important as your physical health.",
        "You are not alone. Reach out if you need someone to talk to.",
        "Mental health matters. Prioritize self-care.",
        "Be kind to yourself. You're doing the best you can.",
        "It's okay to ask for help. #mentalhealthsupport",
        "Your mental health is a priority. Don't ignore it.",
        "Check in with yourself regularly. How are you feeling today?",
        "You're stronger than you think. Keep going. #mentalwellness"
    ]
    
    current_mental_health_captions = Post.query.filter(Post.caption.in_(mental_health_captions)).count()
    if current_mental_health_captions < 10:
        remaining_captions = 10 - current_mental_health_captions
        for _ in range(remaining_captions):
            caption = choice(mental_health_captions)
            new_post = Post(caption=caption, user=current_user.id)
            db.session.add(new_post)
        db.session.commit()
        flash(f'{remaining_captions} mental health captions added!', category='success')

    posts = Post.query.all()
    captions = Post.query.with_entities(Post.caption).all()
    print(captions)
    return render_template("socialMedia.html", user=current_user, posts=posts)


@views.route('/event-signup', methods=['GET','POST'])
@login_required
def event_signup():
    #pip install pip install newsapi-python
    from newsapi import NewsApiClient  
    
    newsAPI = NewsApiClient(api_key='b2c8adec9244439385335aee2daf292e')
    
    all_articles = newsAPI.get_everything(q='charity', page_size=12)
    
    news = [{'title': article['title'], 'url': article['url']} for article in all_articles['articles']]
    
    return render_template("event-signup.html", user=current_user, news=news)
