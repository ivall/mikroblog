from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from blueprints.logout import logout_blueprint
from blueprints.register import register_blueprint
from blueprints.login import login_blueprint
from blueprints.dodajkomentarz import dodajkomentarz_blueprint
from blueprints.dodajwpis import dodajwpis_blueprint
from blueprints.remove import remove_blueprint
from blueprints.wpis import wpis_blueprint
from blueprints.removekom import removekom_blueprint
from blueprints.likesystem import likesystem_blueprint
from forms import WpisForm
from errors import page_not_found


app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

app.register_error_handler(404, page_not_found)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/', methods=['GET'])
def index():
    form = WpisForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `id` DESC")
    wpisy = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    komentarze = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.close()
    return render_template('index.html', wpisy=wpisy, komentarze=komentarze, lajki=likes, form=form)


@app.route('/popularne', methods=['GET'])
def popularne():
    form = WpisForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM wpisy ORDER BY `lajki` DESC")
    wpisy = cur.fetchall()
    cur.execute("SELECT * FROM komentarze ORDER BY `id` DESC")
    komentarze = cur.fetchall()
    cur.execute("SELECT * FROM likes")
    likes = cur.fetchall()
    cur.close()
    return render_template('index.html', wpisy=wpisy, komentarze=komentarze, lajki=likes, form=form)


@app.route('/edit/<postid>', methods=['GET'])
def geteditpost(postid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, tresc FROM wpisy WHERE id=%s AND autor=%s",(postid,session['login'],))
    checkWpis = cur.fetchall()
    if checkWpis:
        staraTresc = checkWpis[0]['tresc']
        form = WpisForm()
        return render_template('edit.html',form=form,postid=postid,staraTresc=staraTresc)
    flash("Wystąpił błąd")
    return redirect(url_for('index'))

@app.route('/edit/<postid>', methods=['POST'])
def editpost(postid):
    form = WpisForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, tresc FROM wpisy WHERE id=%s AND autor=%s",(postid,session['login'],))
    checkWpis = cur.fetchall()
    if checkWpis:
        if form.validate_on_submit():
            tresc = form.wpis.data
            cur.execute("UPDATE wpisy SET tresc=%s WHERE id=%s", (tresc, postid,))
            mysql.connection.commit()
            cur.close()
            return redirect('/wpis/'+postid)
        flash("Minimalna długość wpisu to 5 znaków, a maksymalna 300.")
        return redirect(url_for('index'))
    flash("Wystąpił błąd")
    return redirect(url_for('index'))


app.register_blueprint(likesystem_blueprint)

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
