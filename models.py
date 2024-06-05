from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, db.ForeignKey('project_model.id'), nullable=False)
    project = db.Column(db.String(100), nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    completion_status = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    url_suffix = db.Column(db.String(100), nullable=False)

