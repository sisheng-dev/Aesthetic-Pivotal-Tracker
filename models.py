from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    toggl_api = db.Column(db.String(100), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'toggl_api': self.toggl_api
        }
    
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'), nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'description': self.description,
            'project_id': self.project_id,
            'deadline': self.deadline,
            'user_id': self.user_id,
            'status': self.status,
            'project_title': self.project.project
        }

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    url = db.Column(db.String(100), nullable=False)

    tasks = db.relationship('TaskModel', backref='project', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project': self.project,
            'user_id': self.user_id,
            'url': self.url
        }