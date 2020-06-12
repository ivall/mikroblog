from flask import request, session, redirect, abort
from app import mysql
from flask import Blueprint
import os
remove_blueprint = Blueprint('remove_blueprint', __name__)


@remove_blueprint.route('/remove', methods=['POST'])
def remove():
    post_id = request.form['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM wpisy WHERE id=%s AND autor=%s", (post_id, session['login'],))
    checkRemover = cur.fetchone()
    if checkRemover:
        if os.path.exists("./static/images/"+str(checkRemover['id'])):
            os.remove('./static/images/'+str(checkRemover['id']))
        cur.execute("DELETE FROM wpisy WHERE id=%s", (post_id,))
        cur.execute("DELETE FROM komentarze WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM likes WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM tags WHERE post_id=%s", (post_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(request.referrer)
    return abort