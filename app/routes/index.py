from flask import render_template, session
from app import mysql
from flask import Blueprint
from app.utils.forms import AddPostForm

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/', methods=['GET'])
def index():
    notifications = {}
    form = AddPostForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `id` DESC")
    posts = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    comments = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.execute("SELECT login, admin FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form, users=users)
