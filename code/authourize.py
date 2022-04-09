from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .model import User
from . import db
import random

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    N = 6
    images_ = random.sample(range(10, 46), N * N)
    images = []
    for i in range(0, N * N, N):
        images.append(images_[i:i + N])
    return render_template('signup.html',images=images)

@auth.route('/login')
def login():

    N = 6
    images_ = random.sample(range(10, 46), N * N)
    images = []
    for i in range(0, N * N, N):
        images.append(images_[i:i + N])
    return render_template('login.html',images=images)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    if(request.form.get('row') and request.form.get('column')):
        row = request.form.get('row')
        col = request.form.get('column')
        password = row+col
        print(password, ".....")
    else:
        password_1 = sorted(request.form.getlist('password'))
        password_1 = ''.join(map(str, password_1))
        if len(password_1) < 8:
            flash("password must be a minimum 4 selections from the grid")
            return redirect(url_for('auth.signup'))
        else:
            password = password_1

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Oops! This email address already exists')
        return redirect(url_for('auth.signup'))


    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))


    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    if(request.form.get('row-column')):
        password = request.form.get('row-column')
        print(password,".....")

    else:
        password_1= sorted(request.form.getlist('password'))
        password_1 =''.join(map(str, password_1))
        if len(password_1) < 8:
            flash("password must be a minimum 4 selections from the grid")
            return redirect(url_for('auth.signup'))
        else:
            password = password_1


    remember = True if request.form.get('Remember') else False
    user = User.query.filter_by(email=email).first()


    if not user or not check_password_hash(user.password, password):
        flash('Check login credentials and try again!')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
