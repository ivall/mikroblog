from flask import Blueprint, session, request, jsonify, abort
from .. import create_app
from flask_mysqldb import MySQL
import validators
from functions import getActualTime
add_comment_blueprint = Blueprint('add_comment_blueprint', __name__)

app = create_app()
mysql = MySQL(app)


@add_comment_blueprint.route('/dodaj_komentarz', methods=['POST'])
def dodaj_komentarz():
    content = request.form['inputvalue']
    author = session['login']
    post_id = request.form['post_id']
    if validators.length(content, min=2, max=75):
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
