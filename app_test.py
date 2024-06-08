#!/usr/bin/env python3
# Import the necessary modules
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from forms import LoginForm, RegisterForm, ProjectForm, TaskForm, ProfileForm
from flask_login import login_user, logout_user, login_required, current_user 
from models import db, login_manager, UserModel, TaskModel, ProjectModel
from flask_migrate import Migrate
import re
import uuid

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

#Import and initialize Flask-Migrate
migrate = Migrate(app, db)

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

@app.route('/view-users', methods=['GET'])
def view_users():
    # Query all users
    users = UserModel.query.all()

    # Convert the results to a list of dictionaries so it can be converted to JSON
    users_list = [user.to_dict() for user in users]

    return jsonify({'users': users_list})

@app.route('/view-projects', methods=['GET'])
def view_projects():
    # Query all projects
    projects = ProjectModel.query.all()
    # if not projects:
    #     return "no projects found"
    # else:
    # Convert the results to a list of dictionaries so it can be converted to JSON
    projects_list = [project.to_dict() for project in projects]
    return jsonify({'projects': projects_list})
    

@app.route('/view-tasks', methods=['GET'])
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
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    profile_form=ProfileForm()
    user = UserModel.query.filter_by(id=current_user.id).first()
    if request.method == 'GET':
        user_id = current_user.id
        email = user.email
        toggl_api = user.toggl_api
        return render_template('profile.html', profile_form=profile_form, email = email, toggl_api = toggl_api, user=user)
    if request.method == 'POST':
        # flash("profile_form_posted")
        user_id = current_user.id
        user = UserModel.query.filter_by(id=user_id).first()
        # if profile_form.validate_on_submit():
        # flash("profile_form_validated")
        toggl_api = profile_form.toggl_api.data
        # flash(f'{toggl_api}')
        user.toggl_api = toggl_api
        # flash(f'{user.toggl_api}')
        db.session.commit()
        # flash('API key updated')
        return redirect(url_for('profile'))
        # else:
        #     flash('Invalid API key')
        #     return redirect(url_for('profile'))        

    # return render_template('profile.html', profile_form=profile_form, email = email)
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



@app.route('/home', methods=['GET'])
@login_required
def home():
    project_form = ProjectForm()
    projects = ProjectModel.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', project_form=project_form, projects=projects)

@app.route('/new_project', methods=['POST'])
def new_project():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        title = project_form.projectTitle.data
        user_id = UserModel.query.filter_by(email=session['email']).first().id
        # Generate a unique URL for the project
        url = generate_url_suffix(title)
        # Create a new project in the database
        project = ProjectModel(project=title, user_id=user_id, url=url)
        db.session.add(project)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit-project/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    project_form = ProjectForm()
    project = ProjectModel.query.get(project_id)
    if project and project_form.validate_on_submit():
        project.project = project_form.projectTitle.data
        db.session.commit()
        flash('Project updated successfully')
    else:
        flash('Failed to update project')
    return redirect(url_for('home'))


@app.route('/delete-project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = ProjectModel.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted')
    else:
        flash('Project not found')  # It's good practice to inform the user if the project was not found
    return redirect(url_for('home'))


@app.route('/project/<int:project_id>', methods=['GET'])
@login_required
def tasks(project_id):
    task_form = TaskForm()
    to_do_tasks = TaskModel.query.filter_by(user_id=current_user.id, project_id=project_id, status=0).all()
    in_progress_tasks = TaskModel.query.filter_by(user_id=current_user.id, project_id=project_id, status=1).all()
    done_tasks = TaskModel.query.filter_by(user_id=current_user.id, project_id=project_id, status=2).all()
    if request.method == 'GET':
        return render_template('project.html', task_form=task_form, tasks=tasks, to_do_tasks=to_do_tasks, in_progress_tasks=in_progress_tasks, done_tasks=done_tasks)


@app.route('/project/<int:project_id>', methods=['GET','POST'])
def new_task(project_id):
    task_form = TaskForm()
    if task_form.validate_on_submit():
        title = task_form.taskTitle.data
        description = task_form.taskDescription.data
        deadline = task_form.taskDeadline.data
        # Use the project ID from the URL instead of session['project']
        task = TaskModel(task=title, description=description, deadline=deadline, project_id=project_id, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        # flash('Task added')
    # Redirect to the Tasks page for the specific project
    return redirect(url_for('tasks', project_id=project_id))

@app.route('/edit-task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task_form = TaskForm()
    task = TaskModel.query.get(task_id)
    if task and task_form.validate_on_submit():
        task.task = task_form.taskTitle.data
        task.description = task_form.taskDescription.data
        task.deadline = task_form.taskDeadline.data
        db.session.commit()
        flash('Task updated successfully')
    else:
        flash('Failed to update task')
    return redirect(url_for('tasks', project_id=task.project_id))


@app.route('/update-task-status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    task = TaskModel.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    if 'status' in data:
        task.status = data['status']
        db.session.commit()
        return jsonify({'success': 'Task status updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = TaskModel.query.get(task_id)
    if task is None:
        flash('Task not found')
        return redirect(url_for('index'))  # Adjust as necessary
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted')  # Corrected message
    return redirect(url_for('tasks', project_id=project_id))


def generate_url_suffix(title):
    # Replace spaces in the title with hyphens
    title = title.replace(" ", "-")
    # Generate a unique id
    unique_id = uuid.uuid4()
    # Append the unique id to the title to create the URL suffix
    url_suffix = f"{title}-{unique_id}"
    return url_suffix




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


    
@app.route('/session', methods=['GET'])
def session_view():
    return jsonify(session)






if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='True', port=5000)

