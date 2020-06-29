import pytz
from datetime import datetime


def getActualTime():
    tz = pytz.timezone('Europe/Warsaw')
    actualltime = datetime.now(tz).replace(microsecond=0, tzinfo=None)
    return actualltime


def getPosts(cur, where, order_by):
    cur.execute(f"SELECT * FROM wpisy {where.replace('post_id', 'id')} ORDER BY `{order_by}` DESC")
    posts = cur.fetchall()
    cur.execute(f"SELECT * FROM komentarze {where} ORDER BY `id` DESC")
    comments = cur.fetchall()
    cur.execute(f"SELECT * FROM likes")
    likes = cur.fetchall()
    return posts, comments, likes
