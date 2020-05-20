from flask import Flask, Blueprint, request, session, redirect, flash
from flask_mysqldb import MySQL
from forms import AddPostForm
from functions import getActualTime

add_post_blueprint = Blueprint('add_post_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@add_post_blueprint.route('/dodajwpis', methods=['POST'])
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        content = form.wpis.data
        form.wpis.data = ""
        author = session['login']
        actualtime = getActualTime()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO wpisy (tresc, autor, data) VALUES (%s,%s,%s)", (content, author, actualtime,))
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
        websiteLink = 'http://%s' % request.host
        return redirect(f'{websiteLink}/wpis/{post_id}')
    flash("Minimalna długość wpisu to 5 znaków, a maksymalna 300.")
    return redirect(request.referrer)
