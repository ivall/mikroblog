from flask import Blueprint, redirect, url_for, render_template
from .. import mysql
from ..utils.forms import AddPostForm
from ..utils.functions import getPosts

post_blueprint = Blueprint('post_blueprint', __name__)


@post_blueprint.route('/wpis/<int:postid>', methods=['GET'])
def post(postid):
    form = AddPostForm()
    cur = mysql.connection.cursor()
    post, comments, likes = getPosts(cur, f'WHERE post_id={postid}', 'id')
    if post:
        cur.execute("SELECT login, admin FROM users")
        users = cur.fetchall()
        cur.close()
        return render_template('index.html', posts=post, comments=comments, likes=likes, form=form, users=users)
    return redirect(url_for('index_blueprint.index'))
