from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
from blueprints.logout import logout_blueprint
from blueprints.register import register_blueprint
from blueprints.login import login_blueprint
from blueprints.dodajkomentarz import dodajkomentarz_blueprint
from blueprints.dodajwpis import dodajwpis_blueprint
from blueprints.remove import remove_blueprint
from blueprints.wpis import wpis_blueprint
from blueprints.removekom import removekom_blueprint
from forms import KomentarzForm
from forms import WpisForm

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


def page_not_found(e):
    return redirect(url_for('index'))


app.register_error_handler(404, page_not_found)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/', methods=['GET'])
def index():
    form = WpisForm()
    formk = KomentarzForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `id` DESC")
    wpisy = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    komentarze = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.close()
    return render_template('index.html', wpisy=wpisy, komentarze=komentarze, lajki=likes, form=form, formk=formk)


@app.route('/popularne', methods=['GET'])
def popularne():
    form = WpisForm()
    formk = KomentarzForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `lajki` DESC")
    wpisy = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    komentarze = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.close()
    return render_template('index.html', wpisy=wpisy, komentarze=komentarze, lajki=likes, form=form, formk=formk)


@app.route('/like', methods=['POST'])
def like():
    postid = request.form['postid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id=%s AND post_id=%s", (session['login'], postid,))
    likes = cur.fetchall()
    if not likes:
        cur.execute("SELECT * FROM wpisy WHERE id=%s", (postid,))
        table = cur.fetchone()
        row = table['lajki']
        cur.execute("UPDATE wpisy SET lajki=%s+1 WHERE id=%s", (row, postid,))
        cur.execute("INSERT INTO likes(user_id, post_id) VALUES(%s,%s)", (session['login'], postid,))
        mysql.connection.commit()
        cur.close()
        rowapi = table['lajki'] + 1
        return jsonify({'lajkixd': rowapi})
    return redirect(url_for('index'))


@app.route('/unlike', methods=['POST'])
def unlike():
    postid = request.form['postid']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM likes WHERE user_id=%s AND post_id=%s", (session['login'], postid,))
    likes = cur.fetchall()
    if likes:
        cur.execute("SELECT * FROM wpisy WHERE id=%s", (postid,))
        table = cur.fetchone()
        row = table['lajki']
        cur.execute("DELETE FROM likes WHERE post_id=%s AND user_id=%s", (postid, session['login'],))
        cur.execute("UPDATE wpisy SET lajki=%s-1 WHERE id=%s", (row, postid,))
        mysql.connection.commit()
        cur.close()
        rowapi = table['lajki'] - 1
        return jsonify({'lajkixd': rowapi})
    return redirect(url_for('index'))


app.register_blueprint(wpis_blueprint)

app.register_blueprint(remove_blueprint)

app.register_blueprint(dodajwpis_blueprint)

app.register_blueprint(dodajkomentarz_blueprint)

app.register_blueprint(register_blueprint)

app.register_blueprint(login_blueprint)

app.register_blueprint(logout_blueprint)

app.register_blueprint(removekom_blueprint)

if __name__ == '__main__':
    app.run()
