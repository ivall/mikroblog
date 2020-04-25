from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, validators, TextAreaField, PasswordField


# Dodawanie wpisu
class WpisForm(FlaskForm):
    wpis = TextAreaField('wpis', [validators.DataRequired(), validators.Length(min=5, max=300)])


# Rejestracja
class RejestracjaForm(FlaskForm):
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
