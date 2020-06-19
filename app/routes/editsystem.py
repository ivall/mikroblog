from flask import session, url_for, redirect, flash, render_template
from app import mysql
from flask import Blueprint
from app.utils.forms import AddPostForm

editsystem_blueprint = Blueprint('editsystem_blueprint', __name__)


@editsystem_blueprint.route('/edit/<post_id>', methods=['GET'])
def geteditpost(post_id):
    form = AddPostForm()
    form.wpis.data = ""
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, tresc FROM wpisy WHERE id=%s", (post_id,))
    checkPost = cur.fetchone()
    if checkPost and checkPost['autor'] == session['login'] or checkPost and 'admin' in session:
        oldContent = checkPost['tresc']
        form.wpis.data = oldContent
        return render_template('edit.html', form=form, postid=post_id)
    flash("Wystąpił błąd")
    return redirect(url_for('index_blueprint.index'))


@editsystem_blueprint.route('/edit/<postid>', methods=['POST'])
def editpost(postid):
    form = AddPostForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, tresc FROM wpisy WHERE id=%s", (postid,))
    checkPost = cur.fetchone()
    if checkPost and checkPost['autor'] == session['login'] or checkPost and 'admin' in session:
        if form.validate_on_submit():
            content = form.wpis.data
            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip() != ""]
            string_without_empty_lines = ""
            for line in non_empty_lines:
                string_without_empty_lines += line + "\n"
            content = string_without_empty_lines.rstrip()
            cur.execute("UPDATE wpisy SET tresc=%s WHERE id=%s", (content, postid,))
            mysql.connection.commit()
            cur.close()
            return redirect('/wpis/'+postid)
        flash("Minimalna długość wpisu to 5 znaków, a maksymalna 300.")
        return redirect(url_for('index_blueprint.index'))
    flash("Wystąpił błąd")
    return redirect(url_for('index_blueprint.index'))
