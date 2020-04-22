from flask import Flask, Blueprint, redirect, url_for, render_template
from flask_mysqldb import MySQL, MySQLdb
from forms import WpisForm
wpis_blueprint = Blueprint('wpis_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@wpis_blueprint.route('/wpis/<int:postid>', methods=['GET'])
def wpis(postid):
    form = WpisForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy WHERE id=%s ORDER BY `id` DESC",(postid,))
    wpisy = cur.fetchall()
    if wpisy:
        cur.execute("SELECT * FROM komentarze WHERE post_id=%s ORDER BY `id` DESC",(postid,))
        komentarze = cur.fetchall()
        cur.execute("SELECT * FROM likes WHERE post_id=%s",(postid,))
        likes = cur.fetchall()
        cur.close()
        return render_template('index.html', wpisy=wpisy, komentarze=komentarze, lajki=likes, form=form)
    return redirect(url_for('index'))