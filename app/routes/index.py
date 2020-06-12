from flask import render_template
from flask_mysqldb import MySQL
from .. import create_app
from flask import Blueprint
from forms import AddPostForm

index_blueprint = Blueprint('index_blueprint', __name__)

app = create_app()
mysql = MySQL(app)



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
