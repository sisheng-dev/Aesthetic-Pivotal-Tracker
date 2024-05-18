#!/usr/bin/env python3
# Import the necessary modules
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from forms import LoginForm
from yelp import find_coffee
from flask_login import login_user, logout_user, login_required 
from models import db, login_manager, UserModel

# Create a new Flask application instance
app = Flask(__name__)
app.secret_key='super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

#add user routine
def add_user(email, password):
    user = UserModel(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

# create database with a test user
@app.before_first_request
def create_db():
    if (not os.path.exists('login.db')):
        db.create_all()
        add_user('lhhung@uw.edu', 'password')

# Define a route for the root URL ("/") that returns "Hello World"
@app.route('/home', methods=['GET'])
@login_required
def showCoffeeShops():
    if request.method == 'GET' and 'city' in request.args and request.args.get('city') is not None: 
        session['city'] = request.args.get('city')
    if 'city' in session:
        return render_template('home.html', coffeeShops=find_coffee(city=session['city']))
    return render_template('home.html', coffeeShops=find_coffee())
@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pw = form.password.data
            session['email'] = email
            session['city']='Tacoma'
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(pw):
                login_user(user)
                return render_template('home.html', coffeeShops=find_coffee())
            else:
                flash('Invalid email or password')
                logout_user()
                return redirect(url_for('login'))
    return render_template('login.html',form=form)
@login_manager.unauthorized_handler
def unauthorized():
    flash ('You must be logged in to view that page')
    return redirect(url_for('login'))

# Run the application if this script is being run directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='True', port=5000)
