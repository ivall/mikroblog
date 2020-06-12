from flask import render_template
from app import mysql
from flask import Blueprint
from app.utils.forms import AddPostForm

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/', methods=['GET'])
def index():
    form = AddPostForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `id` DESC")
    posts = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    comments = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form)
