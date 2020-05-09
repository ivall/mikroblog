from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
from forms import RegisterForm
import bcrypt
from flask import Blueprint
register_blueprint = Blueprint('register_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    formr = RegisterForm()
    if request.method == 'POST':
        if formr.validate_on_submit():
            login = formr.nick.data.replace(" ", "")
            email = formr.email.data
            cur = mysql.connection.cursor()
            cur.execute("SELECT login FROM users WHERE login=%s",(login,))
            checkUsername = cur.fetchall()
            cur.execute("SELECT email FROM users WHERE email=%s",(email,))
            checkEmail = cur.fetchall()
            if not checkUsername and not checkEmail:
                password = formr.password.data.encode('utf-8')
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                login = login.replace("/", "")
                if len(login) > 4:
                    cur.execute("INSERT INTO users (login, email, password) VALUES (%s,%s,%s)", (login, email, hash_password,))
                    mysql.connection.commit()
                    session['login'] = login
                    return redirect(url_for('index'))
                flash("Login jest za krótki")
            flash("Użytkownik z takim loginem/emailem już istnieje.")
        flash("Wystąpił błąd z walidacją.")
        return redirect(url_for('register_blueprint.register'))
    elif session.get('login'):
        return redirect(url_for('index'))
    else:
        return render_template('register.html', formr=formr)

