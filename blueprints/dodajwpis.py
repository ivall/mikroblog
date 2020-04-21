from flask import Flask, Blueprint, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL, MySQLdb
from forms import WpisForm

dodajwpis_blueprint = Blueprint('dodajwpis_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@dodajwpis_blueprint.route('/dodajwpis', methods=['POST'])
def dodajwpis():
    form = WpisForm()
    if form.validate_on_submit():
        tresc = form.wpis.data
        form.wpis.data = ""
        autor = session['login']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO wpisy (tresc, autor) VALUES (%s,%s)", (tresc, autor,))
        mysql.connection.commit()
        cur.execute("SELECT id,autor FROM wpisy ORDER BY ID DESC LIMIT 1")
        check = cur.fetchall()
        idwpisu = check[0]['id']
        poprzedniastrona = 'http://%s' % request.host
        return redirect(f'{poprzedniastrona}/wpis/{idwpisu}')
    flash("Minimalna długość wpisu to 5 znaków, a maksymalna 500.")
    return redirect(request.referrer)
