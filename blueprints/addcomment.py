from flask import Flask, Blueprint, session, request, jsonify, abort
from flask_mysqldb import MySQL
import validators
from functions import getActualTime
addcomment_blueprint = Blueprint('addcomment_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@addcomment_blueprint.route('/dodajkomentarz', methods=['POST'])
def dodajkomentarz():
    content = request.form['inputvalue']
    author = session['login']
    post_id = request.form['post_id']
    if validators.length(content, min=2, max=50):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM wpisy WHERE id=%s", (post_id,))
        check = cur.fetchone()
        if check:
            actualtime = getActualTime()
            cur.execute("INSERT INTO komentarze (tresc, autor, data, post_id) VALUES (%s,%s,%s,%s)", (content, author, actualtime, post_id,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM komentarze WHERE autor=%s ORDER BY id DESC LIMIT 1", (author,))
            comment_id = cur.fetchone()
            comment_id = comment_id['id']
            return jsonify({'autor': author, 'tresc': content, 'komid': comment_id})
        return abort
    return abort
