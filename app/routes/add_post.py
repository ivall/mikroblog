from flask import Blueprint, request, session, redirect, flash
from .. import create_app
from flask_mysqldb import MySQL
from forms import AddPostForm
from functions import getActualTime
import os

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
add_post_blueprint = Blueprint('add_post_blueprint', __name__)

app = create_app()
mysql = MySQL(app)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_post_blueprint.route('/dodajwpis', methods=['POST'])
def add_post():
    global imageAttached
    form = AddPostForm()
    if form.validate_on_submit():
        content = form.wpis.data
        lines = content.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        string_without_empty_lines = ""
        for line in non_empty_lines:
            string_without_empty_lines += line + "\n"
        content = string_without_empty_lines.rstrip()
        form.wpis.data = ""
        author = session['login']
        actualtime = getActualTime()
        cur = mysql.connection.cursor()
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                imageAttached = 1
            else:
                imageAttached = 0
        else:
            imageAttached = 0
        cur.execute("INSERT INTO wpisy (tresc, autor, data, img) VALUES (%s,%s,%s,%s)", (content, author, actualtime, imageAttached))
        mysql.connection.commit()
        for word in content.split():
            if word[0] == "#":
                word_without_hashtag = word.lstrip(word[0]).lower()
                cur.execute("SELECT id FROM wpisy WHERE autor=%s ORDER BY id DESC LIMIT 1", (session['login'],))
                post_id = cur.fetchone()
                post_id = post_id['id']
                cur.execute("INSERT INTO tags (tag, post_id) VALUES (%s,%s)", (word_without_hashtag, post_id,))
                mysql.connection.commit()
        cur.execute("SELECT id,autor FROM wpisy ORDER BY ID DESC LIMIT 1")
        check = cur.fetchall()
        post_id = check[0]['id']
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(post_id)))
        websiteLink = 'http://%s' % request.host
        return redirect(f'{websiteLink}/wpis/{post_id}')
    flash("Minimalna długość wpisu to 5 znaków, a maksymalna 550.")
    return redirect(request.referrer)
