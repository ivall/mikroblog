from flask import Flask, Blueprint, request, session, redirect, flash
from flask_mysqldb import MySQL
from forms import AddPostForm
from functions import getActualTime

addpost_blueprint = Blueprint('addpost_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@addpost_blueprint.route('/dodajwpis', methods=['POST'])
def dodajwpis():
    form = AddPostForm()
    if form.validate_on_submit():
        content = form.wpis.data
        form.wpis.data = ""
        author = session['login']
        actualtime = getActualTime()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO wpisy (tresc, autor, data) VALUES (%s,%s,%s)", (content, author, actualtime,))
        mysql.connection.commit()
        cur.execute("SELECT id,autor FROM wpisy ORDER BY ID DESC LIMIT 1")
        check = cur.fetchall()
        post_id = check[0]['id']
        websiteLink = 'http://%s' % request.host
        return redirect(f'{websiteLink}/wpis/{post_id}')
    flash("Minimalna długość wpisu to 5 znaków, a maksymalna 300.")
    return redirect(request.referrer)
