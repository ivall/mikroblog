from flask import render_template, redirect, url_for, flash
from app import mysql
from flask import Blueprint

user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@user_profile_blueprint.route('/profil/<nick>', methods=['GET'])
def profil(nick):
    cur = mysql.connection.cursor()
    cur.execute("SELECT description FROM users WHERE login=%s", (nick,))
    check_user_exists = cur.fetchone()
    if check_user_exists:
        cur.execute("SELECT * FROM wpisy WHERE autor=%s ORDER BY `id` DESC", (nick,))
        posts = cur.fetchall()
        count_posts = len(list(cur))
        cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
        comments = cur.fetchall()
        cur.execute("SELECT * FROM komentarze WHERE autor=%s", (nick,))
        count_comments = len(list(cur))
        cur.execute("SELECT * FROM likes")
        likes = cur.fetchall()
        description = check_user_exists['description']
        cur.close()
        return render_template('profil.html', posts=posts, comments=comments, likes=likes, nick=nick,
                               countComments=count_comments, countPosts=count_posts, description=description)
    flash("Nie znaleziono użytkownika z takim loginem")
    return redirect(url_for('index_blueprint.index'))
