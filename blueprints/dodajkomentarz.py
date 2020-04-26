from flask import Flask, Blueprint, session, request, jsonify, abort
from flask_mysqldb import MySQL
import validators
import pytz
from datetime import datetime
dodajkomentarz_blueprint = Blueprint('dodajkomentarz_blueprint', __name__)

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


@dodajkomentarz_blueprint.route('/dodajkomentarz', methods=['POST'])
def dodajkomentarz():
    tresc = request.form['inputvalue']
    autor = session['login']
    post_id = request.form['post_id']
    if validators.length(tresc, min=2, max=50):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM wpisy WHERE id=%s", (post_id,))
        check = cur.fetchone()
        if check:
            tz = pytz.timezone('Europe/Warsaw')
            actualltime = datetime.now(tz).replace(microsecond=0, tzinfo=None)
            cur.execute("INSERT INTO komentarze (tresc, autor, data, post_id) VALUES (%s,%s,%s,%s)", (tresc, autor, actualltime , post_id,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM komentarze WHERE autor=%s ORDER BY id DESC LIMIT 1", (autor,))
            id = cur.fetchone()
            id = id['id']
            return jsonify({'autor': autor, 'tresc': tresc, 'komid': id})
        return abort
    return abort
