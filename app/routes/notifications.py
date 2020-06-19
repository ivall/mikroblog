from flask import Blueprint, session, jsonify, abort
from app import mysql

notifications_blueprint = Blueprint('notifications_blueprint', __name__)


@notifications_blueprint.route('/powiadomienia', methods=['GET'])
def notifications():
    if 'login' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM notifications WHERE reciver=%s AND readed=%s", (session['login'], 0,))
        notifications = cur.fetchall()
        return jsonify({'notifications': notifications})
    return abort(401)
