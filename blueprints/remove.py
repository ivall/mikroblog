from flask import Flask, request, session, url_for, redirect, flash, abort
from flask_mysqldb import MySQL, MySQLdb
from flask import Blueprint
remove_blueprint = Blueprint('remove_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@remove_blueprint.route('/remove', methods=['POST'])
def remove():
    postid = request.form['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy WHERE id=%s AND autor=%s", (postid, session['login'],))
    checkRemover = cur.fetchall()
    if checkRemover:
        cur.execute("DELETE FROM wpisy WHERE id=%s", (postid,))
        cur.execute("DELETE FROM komentarze WHERE post_id=%s", (postid,))
        cur.execute("DELETE FROM likes WHERE post_id=%s", (postid,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort