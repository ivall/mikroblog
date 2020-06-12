from flask import request, session, jsonify, abort
from .. import create_app
from flask_mysqldb import MySQL
from flask import Blueprint

likesystem_blueprint = Blueprint('likesystem_blueprint', __name__)

app = create_app()
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


@likesystem_blueprint.route('/likes', methods=['POST'])
def likes():
    users = []
    post_id = request.form['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM likes WHERE post_id=%s", (post_id,))
    likes = cur.fetchall()
    if likes:
        for x in likes:
            #  users.append('<a href="/profil/'+x['user_id']+'"'+'>'+x['user_id']+'</a>')
            users.append(x['user_id'])
        return jsonify({'likes': ", ".join(users)})
    return jsonify({'likes': 'Nikt jeszcze nie polubił tego wpisu'})
