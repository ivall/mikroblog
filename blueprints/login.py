from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL, MySQLdb
from flask import Blueprint
import bcrypt

login_blueprint = Blueprint('login_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE login=%s", (login,))
        user = cur.fetchone()
        cur.close()

        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                    session['login'] = user['login']
                    return redirect(url_for('index'))
                else:
                    flash("Niepoprawne hasło.")
                    return redirect(url_for('login_blueprint.login'))
        except:
            flash("Wystąpił błąd autoryzacji.")
            return redirect(url_for('login_blueprint.login'))
    elif session.get('login'):
        return redirect(url_for('index'))
    else:
        return render_template('login.html')
