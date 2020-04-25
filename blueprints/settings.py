from flask import Flask, session, url_for, redirect, flash, render_template
from flask_mysqldb import MySQL
from flask import Blueprint
from forms import ChangeEmail
from forms import ChangePassword
import bcrypt

settings_blueprint = Blueprint('settings_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

@settings_blueprint.route('/ustawienia', methods=['GET'])
def ustawieniaget():
    if session['login']:
        formr = ChangeEmail()
        formp = ChangePassword()
        return render_template('ustawienia.html',formr=formr,formp=formp)
    flash("Wystąpił błąd")
    return redirect(url_for('index'))


@settings_blueprint.route('/zmienemail', methods=['POST'])
def zmienemail():
    if session['login']:
        formr = ChangeEmail()
        if formr.validate_on_submit():
            email = formr.email.data
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET email=%s WHERE login=%s", (email, session['login'],))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('index'))
        flash("Wystąpił błąd")
        return redirect(url_for('index'))
    flash("Wystąpił błąd")
    return redirect(url_for('index'))


@settings_blueprint.route('/zmienhaslo', methods=['POST'])
def zmienhaslo():
    if session['login']:
        formp = ChangePassword()
        if formp.validate_on_submit():
            oldpassword = formp.oldpassword.data.encode('utf-8')
            cur = mysql.connection.cursor()
            cur.execute("SELECT password FROM users WHERE login=%s", (session['login'],))
            oldpasswordcheck = cur.fetchone()
            cur.close()
            if bcrypt.hashpw(oldpassword, oldpasswordcheck['password'].encode('utf-8')) == oldpasswordcheck['password'].encode('utf-8'):
                password = formp.password.data.encode('utf-8')
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET password=%s WHERE login=%s", (hash_password, session['login'],))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('index'))
            flash("Niepoprawne stare hasło")
            return redirect(url_for('index'))
        flash("Wystąpił błąd")
        return redirect(url_for('index'))
    flash("Wystąpił błąd")
    return redirect(url_for('index'))