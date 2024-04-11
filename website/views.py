from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/diary', methods=['GET', 'POST'])
#@login_required
def diary():
    if request.method == 'POST':
        data = request.get_json()
        print(data)  # This will print the JSON data to the console
        # Will sort out data handling here
        return redirect(url_for('views.home'))
    else:
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
