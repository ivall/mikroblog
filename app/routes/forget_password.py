from flask import request, session, url_for, redirect, flash
from .. import mysql, mail
from flask import Blueprint
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import string
import bcrypt
import random

forget_password_blueprint = Blueprint('forget_password_blueprint', __name__)

s = URLSafeTimedSerializer('secretkey')


@forget_password_blueprint.route('/reset', methods=['POST'])
def reset():
    email = request.form['email']
    if email:
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM users WHERE email=%s", (email,))
        userEmail = cur.fetchone()
        if userEmail:
            token = s.dumps(email, salt='password-reset')
            msg = Message('mikroblog.ct8.pl: resetuj hasło', sender='mikroblog@ivall.pl', recipients=[email])
            link = url_for('forget_password_blueprint.reset_token', token=token, _external=True)
            msg.body = 'Otrzymano prośbę o zresetowanie hasła do serwisu https://mikroblog.ct8.pl, link do resetowania hasła: {}'.format(
                link)
            mail.send(msg)
            flash("Wysłano link do resetowania hasła na podany email, link jest ważny 10 minut")
            return redirect(url_for('login_blueprint.login'))
        flash("Nie znaleziono użytkownika z takim emailem")
        return redirect(url_for('login_blueprint.login'))
    flash("Nie podałeś adresu email")
    return redirect(url_for('login_blueprint.login'))


@forget_password_blueprint.route('/reset/<token>')
def reset_token(token):
    if 'login' not in session:
        try:
            email = s.loads(token, salt='password-reset', max_age=600)
        except SignatureExpired:
            flash("Token jest już nieważny")
            return redirect(url_for('login_blueprint.login'))
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        password_for_hash = password.encode('utf-8')
        hash_password = bcrypt.hashpw(password_for_hash, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password=%s WHERE email=%s", (hash_password, email,))
        mysql.connection.commit()
        cur.close()
        msg = Message('mikroblog.ct8.pl: nowe hasło', sender='mikroblog@ivall.pl', recipients=[email])
        msg.body = 'Twoje nowe hasło do logowania: {}'.format(password)
        mail.send(msg)
        flash("Wysłano nowe hasło na emaila")
        return redirect(url_for('login_blueprint.login'))
    return redirect(url_for('index_blueprint.index'))
