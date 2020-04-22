from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL, MySQLdb
from forms import RejestracjaForm
import bcrypt
from flask import Blueprint
register_blueprint = Blueprint('register_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    formr = RejestracjaForm()
    if request.method == 'POST':
        if formr.validate_on_submit():
            login = formr.nick.data.replace(" ", "")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE login=%s",(login,))
            checkUsername = cur.fetchall()
            if not checkUsername:
                email = formr.email.data
                password = formr.password.data.encode('utf-8')
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur.execute("INSERT INTO users (login, email, password) VALUES (%s,%s,%s)", (login, email, hash_password,))
                mysql.connection.commit()
                session['login'] = login
                session['email'] = email
                return redirect(url_for('index'))
            flash("Użytkownik z takim loginem już istnieje.")
        flash("Wystąpił błąd z walidacją.")
        return redirect(url_for('register_blueprint.register'))
    elif session.get('login'):
        return redirect(url_for('index'))
    else:
        return render_template('register.html', formr=formr)
