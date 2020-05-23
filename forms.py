from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, validators, TextAreaField, PasswordField, FileField


# Dodawanie wpisu
class AddPostForm(FlaskForm):
    wpis = TextAreaField('wpis', [validators.DataRequired(), validators.Length(min=5, max=550)])


# Rejestracja
class RegisterForm(FlaskForm):
    nick = StringField('nick', [validators.DataRequired(), validators.Length(min=4, max=28)])
    email = StringField('email', [validators.DataRequired(), validators.email()])
    password = PasswordField('password', [validators.DataRequired()])
    recaptcha = RecaptchaField()


# Zmiana emaila
class ChangeEmail(FlaskForm):
    email = StringField('email', [validators.DataRequired(), validators.email()])


# Zmiana hasła
class ChangePassword(FlaskForm):
    oldpassword = PasswordField('oldpassword', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
