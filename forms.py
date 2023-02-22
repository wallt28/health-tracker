from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', [validators.Length(min=4, max=20)])
    last_name = StringField('last_name', [validators.Length(min=4, max=20)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password',
        validators=[DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')




