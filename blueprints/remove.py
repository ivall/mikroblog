from flask import Flask, request, session, redirect, abort
from flask_mysqldb import MySQL
from flask import Blueprint
remove_blueprint = Blueprint('remove_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@remove_blueprint.route('/remove', methods=['POST'])
def remove():
    post_id = request.form['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy WHERE id=%s AND autor=%s", (post_id, session['login'],))
    checkRemover = cur.fetchall()
    if checkRemover:
        cur.execute("DELETE FROM wpisy WHERE id=%s", (post_id,))
        cur.execute("DELETE FROM komentarze WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM likes WHERE post_id=%s", (post_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort