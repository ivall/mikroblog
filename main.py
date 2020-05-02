from flask import Flask, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from blueprints.logout import logout_blueprint
from blueprints.register import register_blueprint
from blueprints.login import login_blueprint
from blueprints.addcomment import addcomment_blueprint
from blueprints.addpost import addpost_blueprint
from blueprints.remove import remove_blueprint
from blueprints.post import post_blueprint
from blueprints.removecomment import removecomment_blueprint
from blueprints.likesystem import likesystem_blueprint
from blueprints.editsystem import editsystem_blueprint
from blueprints.settings import settings_blueprint
from forms import AddPostForm
from errors import page_not_found

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

app.register_error_handler(404, page_not_found)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/', methods=['GET'])
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


@app.route('/popularne', methods=['GET'])
def popularne():
    form = AddPostForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `lajki` DESC")
    posts = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    comments = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form)


@app.route('/profil/<nick>', methods=['GET'])
def profil(nick):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE login=%s",(nick,))
    checkUserExists = cur.fetchall()
    if checkUserExists:
        cur.execute("SELECT * FROM wpisy WHERE autor=%s ORDER BY `id` DESC",(nick,))
        posts = cur.fetchall()
        countPosts = len(list(cur))
        cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
        comments = cur.fetchall()
        cur.execute("SELECT * FROM komentarze WHERE autor=%s",(nick,))
        countComments = len(list(cur))
        cur.execute("SELECT * FROM likes")
        likes = cur.fetchall()
        cur.close()
        return render_template('profil.html', posts=posts, comments=comments, likes=likes, nick=nick, countComments=countComments, countPosts=countPosts)
    flash("Nie znaleziono użytkownika z takim loginem")
    return redirect(url_for('index'))


app.register_blueprint(settings_blueprint)

app.register_blueprint(editsystem_blueprint)

app.register_blueprint(likesystem_blueprint)

app.register_blueprint(post_blueprint)

app.register_blueprint(remove_blueprint)

app.register_blueprint(addpost_blueprint)

app.register_blueprint(addcomment_blueprint)

app.register_blueprint(register_blueprint)

app.register_blueprint(login_blueprint)

app.register_blueprint(logout_blueprint)

app.register_blueprint(removecomment_blueprint)

if __name__ == '__main__':
    app.run()
