from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
    
class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), Length(min=6, max=40)])
    
class ProjectForm(FlaskForm):
    projectTitle = StringField('Title', validators=[DataRequired(), Length(min=1, max=40)])
    # url = StringField(f'/{projectTitle}', validators=[DataRequired()])
    # submit = SubmitField('submit')

class TaskForm(FlaskForm):
    taskTitle = StringField('title', validators=[DataRequired(), Length(min=1, max=100)])
    taskDescription = StringField('description', validators=[DataRequired(), Length(min=1, max=500)])
    taskDeadline = DateField('deadline', validators=[DataRequired()])
