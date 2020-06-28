from flask import request, session, redirect, abort
from .. import mysql
from flask import Blueprint
import os
remove_blueprint = Blueprint('remove_blueprint', __name__)


@remove_blueprint.route('/remove', methods=['POST'])
def remove_post():
    post_id = request.form['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT autor, id, img FROM wpisy WHERE id=%s", (post_id,))
    check_remover = cur.fetchone()
    if check_remover and check_remover['autor'] == session['login'] or check_remover and 'admin' in session:
        if os.path.exists("app/static/images/"+str(check_remover['img'])) and check_remover['img']:
            os.remove('app/static/images/'+str(check_remover['img']))
        cur.execute("DELETE FROM wpisy WHERE id=%s", (post_id,))
        cur.execute("DELETE FROM komentarze WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM likes WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM tags WHERE post_id=%s", (post_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort(401)
