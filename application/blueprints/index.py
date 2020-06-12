from flask import Flask, render_template
from .. import create_app as app
from flask import Blueprint
from forms import AddPostForm

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
