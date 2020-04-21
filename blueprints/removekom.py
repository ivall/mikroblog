from flask import Flask, request, session, url_for, redirect, flash, abort
from flask_mysqldb import MySQL, MySQLdb
from flask import Blueprint
removekom_blueprint = Blueprint('removekom_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@removekom_blueprint.route('/removekom', methods=['POST'])
def removekom():
    kom_id = request.form['kom_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM komentarze WHERE id=%s AND autor=%s", (kom_id, session['login'],))
    checkRemover = cur.fetchall()
    if checkRemover:
        cur.execute("DELETE FROM komentarze WHERE id=%s", (kom_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort