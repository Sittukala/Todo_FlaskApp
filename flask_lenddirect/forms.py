from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_lenddirect.models import User, Todos
from flask_login import current_user

priorityChoices = [('1', 'High'),('2', 'Medium'),('3', 'Low')]


class UserRegisterForm(FlaskForm):
 userName = StringField('UserName',validators=[DataRequired(), Length(min=2, max=20)])
 emailId = StringField('Email',validators=[DataRequired(), Email()])
 password = PasswordField('Password', validators=[DataRequired()])
 confirmPassword = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
 submit = SubmitField('Sign Up')

 def validate_userName(self,userName):
 	user = User.query.filter_by(userName=userName.data).first()
 	if user:
 		raise ValidationError('Username already exists. Please use a different one.')
 
 def validate_emailId(self,emailId):
 	user = User.query.filter_by(emailId=emailId.data).first()
 	if user:
 		raise ValidationError('Email Id already exists. Please use a different one.')

 
class UserLoginForm(FlaskForm):
    emailId = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UserUpdateForm(FlaskForm):
 userName = StringField('UserName',validators=[DataRequired(), Length(min=2, max=20)])
 emailId = StringField('Email',validators=[DataRequired(), Email()])
 submit = SubmitField('Update')

 def validate_userName(self,userName):
 	if userName.data!= current_user.userName:
	 	user = User.query.filter_by(userName=userName.data).first()
	 	if user:
	 		raise ValidationError('Username already exists. Please use a different one.')
 
 def validate_emailId(self,emailId):
 	if emailId.data != current_user.emailId:
	 	user = User.query.filter_by(emailId=emailId.data).first()
	 	if user:
	 		raise ValidationError('Email Id already exists. Please use a different one.')

class TaskForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority',
                        choices=priorityChoices,validators=[DataRequired()])
    completed = BooleanField('Completed')
    submit = SubmitField('Create')

class UpdateTaskForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority',
                        choices=priorityChoices,validators=[DataRequired()])
    completed = BooleanField('Completed')
    submit = SubmitField('Update')