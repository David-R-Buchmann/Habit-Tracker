from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Contains all available paths concerining the authentification of user login and signup.

@auth.route('/login', methods=['GET', 'POST']) # defines /login as the route for logging in.
def login():
    if request.method == 'POST':
        userName = request.form.get('userName') # gets the username from the request form's corresponding input field
        password = request.form.get('password1') # gets the password from the request form's corresponding input field (only password1 since password1 and password2 need to be identical)

        user = User.query.filter_by(userName=userName).first() # searches for the user amongst all User instances and selects the first entry found
        if user: 
            if check_password_hash(user.password, password): # checks for the hashed password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # remembers the user's login
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User Name does not exist.', category='error')

    return render_template("login.html", user=current_user) # returns the login screen.

@auth.route('/logout') # logs out the user under the route /logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST']) # defines the signup route /sign-up
def sign_up():
    if request.method == 'POST': 
        userName = request.form.get('userName') # gets all necessary information from the request forms
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(userName=userName).first() # searches for the user amongst all User instances and selects the first entry found
        if user:
            flash('User Name already exists.', category='error')
        elif len(userName) < 4: # username must be at least 4 characters long
            flash('User Name must be longer than 3 characters.', category='error')
        elif len(first_name) < 2: # first name must be at least 2 characters long
            flash('First name must be longer than 1 characters.', category='error')
        elif password1 != password2: # passwords must match
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at leaast 7 characters.', category='error')
        else:
            new_user = User(userName=userName, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)