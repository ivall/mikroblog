from flask import render_template, redirect, url_for, flash
from .. import mysql
from flask import Blueprint
from ..utils.functions import getPosts

user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@user_profile_blueprint.route('/profil/<nick>', methods=['GET'])
def profil(nick):
    cur = mysql.connection.cursor()
    cur.execute("SELECT description FROM users WHERE login=%s", (nick,))
    check_user_exists = cur.fetchone()
    if check_user_exists:
        posts, comments, likes = getPosts(cur, f'WHERE autor=\'{nick}\'', 'id')
        count_posts = len(list(posts))
        count_comments = len(list(comments))
        cur.execute("SELECT login, admin FROM users")
        users = cur.fetchall()
        description = check_user_exists['description']
        cur.close()
        return render_template('profil.html', posts=posts, comments=comments, likes=likes, nick=nick,
                               countComments=count_comments, countPosts=count_posts, description=description, users=users)
    flash("Nie znaleziono użytkownika z takim loginem")
    return redirect(url_for('index_blueprint.index'))
