from flask import Flask, session, url_for, redirect, flash, render_template
from flask_mysqldb import MySQL
from flask import Blueprint
from forms import WpisForm

editsystem_blueprint = Blueprint('editsystem_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

@editsystem_blueprint.route('/edit/<postid>', methods=['GET'])
def geteditpost(postid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, tresc FROM wpisy WHERE id=%s AND autor=%s",(postid,session['login'],))
    checkWpis = cur.fetchall()
    if checkWpis:
        staraTresc = checkWpis[0]['tresc']
        form = WpisForm()
        return render_template('edit.html',form=form,postid=postid,staraTresc=staraTresc)
    flash("Wystąpił błąd")
    return redirect(url_for('index'))

@editsystem_blueprint.route('/edit/<postid>', methods=['POST'])
def editpost(postid):
    form = WpisForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, tresc FROM wpisy WHERE id=%s AND autor=%s",(postid,session['login'],))
    checkWpis = cur.fetchall()
    if checkWpis:
        if form.validate_on_submit():
            tresc = form.wpis.data
            cur.execute("UPDATE wpisy SET tresc=%s WHERE id=%s", (tresc, postid,))
            mysql.connection.commit()
            cur.close()
            return redirect('/wpis/'+postid)
        flash("Minimalna długość wpisu to 5 znaków, a maksymalna 300.")
        return redirect(url_for('index'))
    flash("Wystąpił błąd")
    return redirect(url_for('index'))