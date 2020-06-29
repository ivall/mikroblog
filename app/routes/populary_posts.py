from flask import render_template
from .. import mysql
from flask import Blueprint
from ..utils.forms import AddPostForm
from ..utils.functions import getPosts

populary_posts_blueprint = Blueprint('populary_posts_blueprint', __name__)


@populary_posts_blueprint.route('/popularne', methods=['GET'])
def populary():
    form = AddPostForm()
    cur = mysql.connection.cursor()
    posts, comments, likes = getPosts(cur, '', 'lajki')
    cur.execute("SELECT login, admin FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form, users=users)
