from flask import Flask, Blueprint, session, redirect, url_for, request, flash
from flask_mysqldb import MySQL, MySQLdb
from forms import KomentarzForm
dodajkomentarz_blueprint = Blueprint('dodajkomentarz_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)



@dodajkomentarz_blueprint.route('/dodajkomentarz', methods=['POST'])
def dodajkomentarz():
    formk = KomentarzForm()
    if formk.validate_on_submit():
        tresc = formk.komentarz.data
        autor = session['login']
        post_id = request.form['postid']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO komentarze (tresc, autor, post_id) VALUES (%s,%s,%s)", (tresc, autor, post_id))
        mysql.connection.commit()
        return redirect(request.referrer)
    flash("Minimalna długość komentarza to 2 znaki, a maksymalna 50.")
    return redirect(request.referrer)