from flask import render_template, request, session, url_for, redirect, flash
from .. import mysql
from flask import Blueprint
import bcrypt

login_blueprint = Blueprint('login_blueprint', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE login=%s", (login,))
        user = cur.fetchone()
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
                return redirect(url_for('login_blueprint.login'))
    elif session.get('login'):
        return redirect(url_for('index_blueprint.index'))
    else:
        return render_template('login.html')
