from flask import render_template, session
from .. import mysql
from flask import Blueprint
from ..utils.forms import AddPostForm
from ..utils.functions import getPosts

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/', methods=['GET'])
def index():
    form = AddPostForm()
    cur = mysql.connection.cursor()
    posts, comments, likes = getPosts(cur, '', 'id')
    cur.execute("SELECT login, admin FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form, users=users)
