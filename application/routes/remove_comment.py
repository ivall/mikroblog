from flask import Flask, request, session, redirect, abort
from flask_mysqldb import MySQL
from flask import Blueprint
remove_comment_blueprint = Blueprint('remove_comment_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@remove_comment_blueprint.route('/removekom', methods=['POST'])
def remove_comment():
    comment_id = request.form['kom_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM komentarze WHERE id=%s AND autor=%s", (comment_id, session['login'],))
    checkRemover = cur.fetchall()
    if checkRemover:
        cur.execute("DELETE FROM komentarze WHERE id=%s", (comment_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort