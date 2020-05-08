from flask import Flask, request, session, url_for, redirect, jsonify, abort
from flask_mysqldb import MySQL
from flask import Blueprint

likesystem_blueprint = Blueprint('likesystem_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@likesystem_blueprint.route('/like', methods=['POST'])
def like():
    post_id = request.form['postid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id=%s AND post_id=%s", (session['login'], post_id,))
    likes = cur.fetchall()
    if not likes:
        cur.execute("SELECT * FROM wpisy WHERE id=%s", (post_id,))
        table = cur.fetchone()
        row = table['lajki']
        cur.execute("UPDATE wpisy SET lajki=%s+1 WHERE id=%s", (row, post_id,))
        cur.execute("INSERT INTO likes(user_id, post_id) VALUES(%s,%s)", (session['login'], post_id,))
        mysql.connection.commit()
        cur.close()
        likes = table['lajki'] + 1
        return jsonify({'likes': likes})
    return abort


@likesystem_blueprint.route('/unlike', methods=['POST'])
def unlike():
    post_id = request.form['postid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id=%s AND post_id=%s", (session['login'], post_id,))
    likes = cur.fetchall()
    if likes:
        cur.execute("SELECT * FROM wpisy WHERE id=%s", (post_id,))
        table = cur.fetchone()
        row = table['lajki']
        cur.execute("DELETE FROM likes WHERE post_id=%s AND user_id=%s", (post_id, session['login'],))
        cur.execute("UPDATE wpisy SET lajki=%s-1 WHERE id=%s", (row, post_id,))
        mysql.connection.commit()
        cur.close()
        likes = table['lajki'] - 1
        return jsonify({'likes': likes})
    return abort
