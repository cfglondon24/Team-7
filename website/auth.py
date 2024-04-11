from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('rememberMe')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=(remember_me=='on'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        location = request.form.get('location')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='danger')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(first_name) < 2:
            flash('Firstname must be greater than 1 character.', category='danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='danger')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='danger')
        else:
            if password1 == 'supporter':
                role = RoleEnum.SUPPORTER
            else:
                role = RoleEnum.PATIENT
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), location=location, role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('sign_up.html', user=current_user)