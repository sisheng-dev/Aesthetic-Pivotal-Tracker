#!/usr/bin/env python3
# Import the necessary modules
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from forms import LoginForm, RegisterForm, ProjectForm, TaskForm
from yelp import find_coffee
from flask_login import login_user, logout_user, login_required 
from models import db, login_manager, UserModel #, TaskModel, ProjectModel

# Create a new Flask application instance
app = Flask(__name__)
app.secret_key='super secret key'

DBUSER = 'dwools'
DBPASS = 'password'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'pglogindb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

#add user routine
def add_user(email, password):
    existing_user = UserModel.query.filter_by(email=email).first()
    if existing_user:
        # print(f"User with email '{email}' already exists.")
        return existing_user
    else:
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
        add_user('dwools@uw.edu', 'password')


# @app.route('/home', methods=['GET'])
# @login_required
# def showCoffeeShops():
#     if request.method == 'GET' and 'city' in request.args and request.args.get('city') is not None: 
#         session['city'] = request.args.get('city')
#     if 'city' in session:
#         return render_template('home.html', coffeeShops=find_coffee(city=session['city']))
#     return render_template('home.html', coffeeShops=find_coffee())



@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pw = form.password.data
            session['email'] = email
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(pw):
                login_user(user)
                # return render_template('home1.html', projects=ProjectModel.query.all())
                return render_template('home.html')
            else:
                flash('Invalid email or password')
                logout_user()
                return redirect(url_for('login'))
    return render_template('login.html',form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pw = form.password.data
            session['email'] = email
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email, pw)
                user = UserModel.query.filter_by(email=email).first()
                login_user(user)
                # return render_template('home1.html', projects=ProjectModel.query.all())
                return render_template('home.html', coffeeShops=find_coffee())
            else:
                flash('Email already exists')
                return redirect(url_for('register'))                
    return render_template('login.html',form=form)

@app.route('/logout', methods=['GET'])
def logout():
    """
    Logout the user. Add another entry to the navbar for a logout function. You need to create a new route in app.py (/logout) and have it pop off all the elements in the session object.
    """
    
    print(session)
    session.clear()
    print(session)
   
    return redirect('/login') 

@login_manager.unauthorized_handler
def unauthorized():
    flash ('You must be logged in to view that page')
    return redirect(url_for('login'))

@app.route('/project', methods=['GET'])
def project():
    if request.method == 'GET':
        return render_template('project.html')

@app.route('/home', methods=['GET'])
# @login_required
def home():
    if request.method == 'GET':
        return render_template('home.html')

# @app.route('/new_project', methods=['POST'])
# def new_project():
#     form = ProjectForm()
#     if request.method == 'POST':
#         project = form.project.data
#         session['project'] = project
#         db.session.add(project)
#         db.session.commit()
#         flash('Project added')
#     render_template('home.html', project=form)

# @app.route('/new_task', methods=['POST'])
# def new_task():
#     form = TaskForm()
#     if request.method == 'POST':
#         task = form.task.data
#         session['task'] = task
#         session['completion_status'] = form.completion_status.data
#         task.user_id = current_user.id
#         db.session.add(task)
#         db.session.commit()
#         flash('Task added')        
#     return render_template('project.html', task=form)

# @app.route('/project', methods=['GET'])
# def get_task_list():
#     tasks = ProjectModel.query.get(session['tasks'])
    

#     return render_template('project.html', project=project)

# @app.route('/home', methods=['GET'])
# def get_project_list():
#     user_id = 
#     user = UserModel.query.filter_by(email=email).first()
#     if ProjectModel.user_id == current_user.id:
#         projects = ProjectModel.query.get(session['projects'])
#         return render_template('home1.html', projects=projects)

# # @app.route('/complete_task', methods=['POST'])
# # def complete_task():
# #     task = TaskForm()
# #     if request.method == 'POST':
# #         task = TaskModel.query.get(TaskModel.id)
# #         task.completion_status = True
# #         db.session.commit()
# #         flash('Task completed')




# @app.route('/delete_task/<int:task_id>', methods=['POST'])
# def delete_task(task_id):
#     task = TaskModel.query.get(task_id)
#     if task:
#         db.session.delete(task)
#         db.session.commit()
#         flash('Task deleted')
#     return redirect(url_for('home'))

# @app.route('/delete_project', methods=['POST'])
# def delete_project():
#     project = ProjectModel.query.get(session['project'])
#     if request.method == 'POST':
#         db.session.delete(project)
#         db.session.commit()
#         flash('Project deleted')
#     return redirect(url_for('home'))








# Run the application if this script is being run directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='True', port=5000)

