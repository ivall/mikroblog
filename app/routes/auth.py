from flask import render_template, request, session, url_for, redirect, flash, Blueprint
from .. import mysql
from ..utils.forms import RegisterForm
import bcrypt

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    formr = RegisterForm()
    if request.method == 'POST':
        if formr.validate_on_submit():
            login = formr.nick.data.replace(" ", "")
            email = formr.email.data
            cur = mysql.connection.cursor()
            cur.execute("SELECT login FROM users WHERE login=%s OR email=%s", (login,email,))
            check_user = cur.fetchall()
            if not check_user and not check_user:
                password = formr.password.data.encode('utf-8')
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur.execute("INSERT INTO users (login, email, password, ip) VALUES (%s,%s,%s,%s)",
                            (login, email, hash_password, request.remote_addr))
                mysql.connection.commit()
                session['login'] = login
                return redirect(url_for('index_blueprint.index'))
            flash("Użytkownik z takim loginem/emailem już istnieje.")
            return redirect(url_for('auth_blueprint.register'))
        flash("Wystąpił błąd z walidacją. Dozwoloną są tylko znaki A-Z oraz cyfry.")
        return redirect(url_for('auth_blueprint.register'))
    elif session.get('login'):
        return redirect(url_for('index_blueprint.index'))
    else:
        return render_template('register.html', formr=formr)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE login=%s", (login,))
        user = cur.fetchone()
        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    session['login'] = user['login']

                    cur.execute("UPDATE users SET ip=%s WHERE id=%s", (request.remote_addr, user['id']))
                    mysql.connection.commit()
                    cur.close()
                    if user['admin']:
                        session['admin'] = True
                    return redirect(url_for('index_blueprint.index'))
                else:
                    flash("Niepoprawne hasło.")
                    return redirect(url_for('auth_blueprint.login'))
        except:
            flash("Wystąpił błąd autoryzacji.")
            return redirect(url_for('auth_blueprint.login'))
    elif session.get('login'):
        return redirect(url_for('index_blueprint.index'))
    else:
        return render_template('login.html')


@auth_blueprint.route('/wyloguj')
def logout():
    session.clear()
    return redirect(url_for('index_blueprint.index'))