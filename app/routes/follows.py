from flask import session, render_template, request, abort, redirect, url_for, flash
from app import mysql
from flask import Blueprint
from app.utils.forms import AddPostForm

follows_blueprint = Blueprint('follows_blueprint', __name__)

@follows_blueprint.route('/obserwowane', methods=['GET'])
def follows():
    if 'login' in session:
        tags_list = []
        id_of_posts = []
        form = AddPostForm()
        cur = mysql.connection.cursor()
        cur.execute("SELECT tag FROM obserwowanetagi WHERE user=%s",(session['login'],))
        tags = cur.fetchall()
        if tags:
            for tag in tags:
                tags_list.append(tag['tag'])
            cur.execute("SELECT * FROM tags WHERE tag IN %s",(tags_list,))
            posts_id = cur.fetchall()
            if posts_id:
                for post_id in posts_id:
                    id_of_posts.append(post_id['post_id'])
                cur.execute("SELECT * FROM wpisy WHERE id IN %s ORDER BY `id` DESC",(id_of_posts,))
                posts = cur.fetchall()
                cur.execute("SELECT * FROM komentarze WHERE post_id IN %s ORDER BY `id` DESC",(id_of_posts,))
                comments = cur.fetchall()
                cur.execute("SELECT * FROM likes WHERE post_id IN %s",(id_of_posts,))
                likes = cur.fetchall()
                cur.close()
                return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form)
            flash("Jeszcze nic nie obserwujesz")
            return redirect(url_for('index_blueprint.index'))
        flash("Jeszcze nic nie obserwujesz")
        return redirect(url_for('index_blueprint.index'))
    return redirect(url_for('index_blueprint.index'))


@follows_blueprint.route('/obserwuj', methods=['POST'])
def follow():
    tag = request.form['tag']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM obserwowanetagi WHERE user=%s AND tag=%s", (session['login'], tag,))
    checkFollow = cur.fetchall()
    if not checkFollow:
        cur.execute("INSERT INTO obserwowanetagi(user, tag) VALUES(%s,%s)", (session['login'], tag,))
        mysql.connection.commit()
        cur.close()
        return 'test'
    return abort


@follows_blueprint.route('/przestan_obserwowac', methods=['POST'])
def unlike():
    tag = request.form['tag']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM obserwowanetagi WHERE user=%s AND tag=%s", (session['login'], tag,))
    checkFollow = cur.fetchall()
    if checkFollow:
        cur.execute("DELETE FROM obserwowanetagi WHERE tag=%s AND user=%s", (tag, session['login'],))
        mysql.connection.commit()
        cur.close()
        return 'test'
    return abort


@follows_blueprint.route('/tag/<tagname>')
def tag(tagname):
    form = AddPostForm()
    list_posts = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT post_id FROM tags WHERE tag=%s", (tagname,))
    tags = cur.fetchall()
    if tags:
        for post_id in tags:
            list_posts.append(post_id['post_id'])
        cur.execute("SELECT * FROM wpisy WHERE id IN %s ORDER BY `id` DESC", (list_posts,))
        posts = cur.fetchall()
        cur.execute("SELECT * FROM komentarze WHERE post_id IN %s ORDER BY `id` DESC", (list_posts,))
        comments = cur.fetchall()
        cur.execute("SELECT * FROM likes WHERE post_id IN %s", (list_posts,))
        likes = cur.fetchall()
        cur.execute("SELECT  * FROM obserwowanetagi")
        follows = cur.fetchall()
        cur.close()
        return render_template('index.html', posts=posts, comments=comments, likes=likes, form=form, tag=tagname,
                               follows=follows)
    flash("Taki tag jeszcze nie istnieje")
    return redirect(url_for('index_blueprint.index'))
