from flask import request, session, redirect, abort
from .. import mysql
from flask import Blueprint
import os
remove_blueprint = Blueprint('remove_blueprint', __name__)


@remove_blueprint.route('/remove', methods=['POST'])
def remove():
    post_id = request.form['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, id, img FROM wpisy WHERE id=%s", (post_id,))
    checkRemover = cur.fetchone()
    if checkRemover and checkRemover['autor'] == session['login'] or checkRemover and 'admin' in session:
        if os.path.exists("app/static/images/"+str(checkRemover['img'])) and checkRemover['img']:
            os.remove('app/static/images/'+str(checkRemover['img']))
        cur.execute("DELETE FROM wpisy WHERE id=%s", (post_id,))
        cur.execute("DELETE FROM komentarze WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM likes WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM tags WHERE post_id=%s", (post_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort(401)
