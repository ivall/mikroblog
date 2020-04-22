from flask import Flask, request, session, url_for, redirect, jsonify
from flask_mysqldb import MySQL, MySQLdb
from flask import Blueprint

likesystem_blueprint = Blueprint('likesystem_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@likesystem_blueprint.route('/like', methods=['POST'])
def like():
    postid = request.form['postid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id=%s AND post_id=%s", (session['login'], postid,))
    likes = cur.fetchall()
    if not likes:
        cur.execute("SELECT * FROM wpisy WHERE id=%s", (postid,))
        table = cur.fetchone()
        row = table['lajki']
        cur.execute("UPDATE wpisy SET lajki=%s+1 WHERE id=%s", (row, postid,))
        cur.execute("INSERT INTO likes(user_id, post_id) VALUES(%s,%s)", (session['login'], postid,))
        mysql.connection.commit()
        cur.close()
        rowapi = table['lajki'] + 1
        return jsonify({'lajkixd': rowapi})
    return redirect(url_for('index'))


@likesystem_blueprint.route('/unlike', methods=['POST'])
def unlike():
    postid = request.form['postid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id=%s AND post_id=%s", (session['login'], postid,))
    likes = cur.fetchall()
    if likes:
        cur.execute("SELECT * FROM wpisy WHERE id=%s", (postid,))
        table = cur.fetchone()
        row = table['lajki']
        cur.execute("DELETE FROM likes WHERE post_id=%s AND user_id=%s", (postid, session['login'],))
        cur.execute("UPDATE wpisy SET lajki=%s-1 WHERE id=%s", (row, postid,))
        mysql.connection.commit()
        cur.close()
        rowapi = table['lajki'] - 1
        return jsonify({'lajkixd': rowapi})
    return redirect(url_for('index'))