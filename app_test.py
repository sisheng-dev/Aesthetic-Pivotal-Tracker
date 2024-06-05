#!/usr/bin/env python3
# Import the necessary modules
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from forms import LoginForm, RegisterForm, ProjectForm, TaskForm
from yelp import find_coffee
from flask_login import login_user, logout_user, login_required, current_user 
from models import db, login_manager, UserModel, TaskModel, ProjectModel
import re

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

@app.route('/')
def blank():
    return redirect(url_for('home'))


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
def create_user_db():
    if (not os.path.exists('login.db')):
        db.create_all()
        add_user('dwools@uw.edu', 'password')

@app.route('/reset_db')
def reset_db():
    db.drop_all()
    db.create_all()
    add_user('dwools@uw.edu', 'password')
    return "Database reset"        

@app.route('/view_users', methods=['GET'])
def view_users():
    # Query all users
    users = UserModel.query.all()

    # Convert the results to a list of dictionaries so it can be converted to JSON
    users_list = [user.to_dict() for user in users]

    return jsonify({'users': users_list})

@app.route('/view_projects', methods=['GET'])
def view_projects():
    # Query all projects
    projects = ProjectModel.query.all()
    if not projects:
        return "no projects found"
    else:
    # Convert the results to a list of dictionaries so it can be converted to JSON
        projects_list = [project.to_dict() for project in projects]
        return jsonify({'projects': projects_list})
    

@app.route('/view_tasks', methods=['GET'])
def view_tasks():
    # Query all tasks
    tasks = TaskModel.query.all()

    # Convert the results to a list of dictionaries so it can be converted to JSON
    tasks_list = [task.to_dict() for task in tasks]

    return jsonify({'tasks': tasks_list})



# @app.route('/home', methods=['GET'])
# @login_required
# def showCoffeeShops():
#     if request.method == 'GET' and 'city' in request.args and request.args.get('city') is not None: 
#         session['city'] = request.args.get('city')
#     if 'city' in session:
#         return render_template('home.html', coffeeShops=find_coffee(city=session['city']))
#     return render_template('home.html', coffeeShops=find_coffee())

@app.route('/kanban', methods=['GET'])
def kanban():
    if request.method == 'GET':
        return render_template('kanban.html')
    


# return redirect(url_for('index', param1='value1', param2='value2'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form=LoginForm()
    project_form=ProjectForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            pw = login_form.password.data
            session['email'] = email
            user = UserModel.query.filter_by(email=email).first()
            user_id = user.id
            projects=ProjectModel.query.filter_by(user_id=user_id).all()
            if user is not None and user.check_password(pw):
                login_user(user)
                # return render_template('home1.html', projects=ProjectModel.query.all())
                # render_template('home.html', project_form=project_form, projects = projects)
                return redirect(url_for('home', login_form=login_form, project_form=project_form, projects = projects))
                
            else:
                flash('Invalid email or password')
                logout_user()
                return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)





@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form=RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
            email = register_form.email.data
            pw = register_form.password.data
            session['email'] = email
            user = UserModel.query.filter_by(email=email).first() # "user" is now a database of dictionaries. {id = ..., email = ..., password = ...}
            user_id = user["id"]
            if user is None:
                add_user(email, pw)
                user = UserModel.query.filter_by(email=email).first()
                login_user(user)
                # return render_template('home1.html', projects=ProjectModel.query.all())
                return render_template('home.html')
            else:
                flash('Email already exists')
                return redirect(url_for('register'))                
    return render_template('registration.html',register_form=register_form)



@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    project_form = ProjectForm()
    projects = ProjectModel.query.filter_by(user_id=current_user.id).all()
    if request.method == 'GET':
        # login_form = request.args.get('login_form')
        # projects = request.args.get('projects')
        # project_title = project_form.projectTitle.data
    # return render_template('home.html', project_form=project_form, login_form=login_form, projects=projects)
        return render_template('home.html', project_form=project_form, projects=projects)
  


@app.route('/delete-project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = ProjectModel.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted')
    return redirect(url_for('home'))

def generate_url_suffix(title):
    # Convert title to lowercase
    title = title.lower()
    # Replace spaces with hyphens
    title = title.replace(' ', '-')
    # Remove non-alphanumeric characters (except hyphens)
    title = re.sub(r'[^a-z0-9-]', '', title)
    return title




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
    
@app.route('/session', methods=['GET'])
def session_view():
    return jsonify(session)


@app.route('/home', methods=['GET', 'POST'])
def new_project():
    project_form = ProjectForm()
    if request.method == 'POST':
        if project_form.validate_on_submit():
            title = project_form.projectTitle.data
            user_id = UserModel.query.filter_by(email=session['email']).first().id
            # Generate a unique URL for the project
            url = generate_url_suffix(title)
            # Create a new project in the database
            project = ProjectModel(project=title, user_id=user_id, url=url)
            flash(f'Project added: {project.project}')
            flash(f'UserID: {project.user_id}')
            db.session.add(project)
            db.session.commit()
            # Create an empty database of tasks for the project
            # flash('Project added')
        else:
            return "Form did not validate"
    return redirect(url_for('home', project_form=project_form))

@app.route('/project', methods=['POST'])
def new_task():
    task_form = TaskForm()
    if request.method == 'POST':
        if task_form.validate_on_submit():
            title = task_form.title.data
            description = task_form.description.data
            deadline = task_form.deadline.data
            completion_status = False
            project_id =  ProjectModel.query.get(session['project']).id
            project_url = ProjectModel.query.get(session['project']).url
            task = TaskModel(task=title, description=description, deadline=deadline, completion_status=completion_status, project_id=project_id, user_id=current_user.id)
            # project.tasks.append(task)
            db.session.add(task)
            db.session.commit()
            flash('Task added')
    return render_template(f'{project_url}', task_form=task_form)



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

# @app.route('/delete-project', methods=['GET'])
# def delete_project():
#     project = ProjectModel.query.get(project.id)
#     if request.method == 'GET':
#         flash(f'{project.project}')

#         # db.session.delete(project)
#         # db.session.commit()
#         flash('Project deleted')
#     return redirect(url_for('home'))





# When a user logs in with a valid email and password, they should be redirected to /home. If a user is not logged in, they should be redirected to /login. If a user is logged in and tries to access /login, they should be redirected to /home. If a user is not logged in and tries to access /home, they should be redirected to /login. If a user is logged in and tries to access /register, they should be redirected to /home. If a user is not logged in and tries to access /register, they should be redirected to /register. If a user is logged in and tries to access /logout, they should be redirected to /login. If a user is not logged in and tries to access /logout, they should be redirected to /login.


# Write a method called new_project() that will add a new project to the database. This method should be accessible via the /home route. This method should only be accessible to logged in users. If a user is not logged in, they should be redirected to /login. If a user is logged in and tries to access /login, they should be redirected to /home. If a user is logged in and tries to access /register, they should be redirected to /home. If a user is not logged in and tries to access /register, they should be redirected to /register. If a user is logged in and tries to access /logout, they should be redirected to /home. If a user is not logged in and tries to access /logout, they should be redirected to /login. The method should create an empty database of tasks specific for the given project. The method should also add the project to the database. The project should have a title and a unique URL. The method should return a template called home.html with the project added to the list of projects. The project should be displayed as a link that will take the user to the project page. The project page should display all the tasks associated with the project. The project page should have a form to add a new task to the project. The task should have a title, description, and end date. The task should have a completion status that defaults to False. The task should have a button to mark the task as complete. The task should have a button to delete the task. The project page should have a button to delete the project. The project page should have a button to return to the home page. The home page should have a button to log out. The home page should have a button to add a new project. The home page should have a button to view all projects. The home page should have a button to view all tasks. The home page should have a button to view all completed tasks. The home page should have a button to view all incomplete tasks. The home page should have a button to view all tasks due today. The home page should have a button to view all tasks due this week. The home page should have a button to view all tasks due this month. The home page should have a button to view all tasks due this year. The home page should have a button to view all tasks due in the future. The home page should have a button to view all tasks due in the past. The home page should have a button to view all tasks due in the next hour. The home page should have a button to view all tasks due in the next day. The home page should have a button to view all tasks due in the next week. The home page should have a button to view all tasks due in the next month. The home page should have a button to view all tasks due in the next year. The home page should have a button to view all tasks due in the past hour. The home page should have a button to view all tasks due in the past day. The home page should have a button to view all tasks due in the past week. The home page should have a button to view all tasks due in the past month. The home page should have a button to view all tasks due in the past year.

# Run the application if this script is being run directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='True', port=5000)

