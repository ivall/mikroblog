from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_socketio import join_room, leave_room, send, emit
from app import mysql, socketio

pm_system_blueprint = Blueprint('pm_system_blueprint', __name__)


@pm_system_blueprint.route('/chat/<sender>/<reciver>', methods=['GET','POST'])
def chat(sender, reciver):
    if request.method == 'GET' and 'login' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE login=%s",(reciver,))
        check_reciver = cur.fetchone()
        if sender == session['login'] and check_reciver and reciver != session['login']:
            cur.execute("SELECT id FROM rooms WHERE sender=%s AND reciver=%s OR sender=%s AND reciver=%s",
                        (sender,reciver,reciver,sender,))
            check_room = cur.fetchone()
            if not check_room:
                cur.execute("INSERT INTO rooms (sender,reciver) VALUES (%s,%s)", (sender,reciver,))
                cur.execute("SELECT id FROM rooms WHERE sender=%s AND reciver=%s OR sender=%s AND reciver=%s",
                            (sender, reciver, reciver, sender,))
                check_room = cur.fetchone()
                mysql.connection.commit()
            room = check_room['id']
            cur.execute("SELECT id FROM notifications WHERE sender=%s AND reciver=%s AND type=%s AND readed=%s",(reciver, sender, 'private_message', 0))
            check_notifications = cur.fetchall()
            if check_notifications:
                cur.execute("DELETE FROM notifications WHERE sender=%s AND reciver=%s AND type=%s AND readed=%s",(reciver, sender, 'private_message', 0))
                mysql.connection.commit()
            cur.execute("SELECT * FROM messages WHERE room_id=%s",(room,))
            old_messages = cur.fetchall()
            return render_template('chat.html', room=room, old_messages=old_messages, reciver=reciver)
        return redirect(url_for('index_blueprint.index'))
    return redirect(url_for('index_blueprint.index'))


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)


@socketio.on('message')
def handle_message(data):
    if data['message']:
        sender = session['login']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM notifications WHERE sender=%s AND reciver=%s AND type=%s AND readed=%s",
                    (sender, data['reciver'], 'private_message', 0))
        check_notifications = cur.fetchall()
        if not check_notifications:
            cur.execute("INSERT INTO notifications (sender,reciver,type,readed) VALUES (%s,%s,%s,%s)",
                        (sender, data['reciver'], 'private_message', 0))
        cur.execute("INSERT INTO messages (sender, room_id, content) VALUES (%s,%s,%s)",
                    (sender, data['room'], data['message'],))
        mysql.connection.commit()
        emit('message', (data['message'], sender), room=data['room'])
