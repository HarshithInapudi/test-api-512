from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

#creating classes for form-type pages

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class SMS(FlaskForm):
	from_ = StringField('From')
	to = StringField('To')
	text = StringField('Text')
	submit = SubmitField('SEND')