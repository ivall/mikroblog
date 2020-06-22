from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_socketio import SocketIO
from logging import FileHandler, WARNING
from flask_limiter import Limiter
from werkzeug.exceptions import RequestEntityTooLarge
from app.utils.errors import ratelimit_handler

mysql = MySQL()
mail = Mail()
socketio = SocketIO()
limiter = Limiter()


def create_app():
    from app.utils.errors import page_not_found
    from app.utils.errors import method_not_allowed
    app = Flask(__name__)
    app.config.from_object('config')

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(413, RequestEntityTooLarge)
    app.register_error_handler(429, ratelimit_handler)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    mysql.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    limiter.init_app(app)
    
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)

    from .routes.logout import logout_blueprint
    from .routes.register import register_blueprint
    from .routes.login import login_blueprint
    from .routes.add_comment import add_comment_blueprint
    from .routes.add_post import add_post_blueprint
    from .routes.remove import remove_blueprint
    from .routes.post import post_blueprint
    from .routes.remove_comment import remove_comment_blueprint
    from .routes.likesystem import likesystem_blueprint
    from .routes.editsystem import editsystem_blueprint
    from .routes.settings import settings_blueprint
    from .routes.follows import follows_blueprint
    from .routes.populary_posts import populary_posts_blueprint
    from .routes.forget_password import forget_password_blueprint
    from .routes.user_profile import user_profile_blueprint
    from .routes.index import index_blueprint
    from .routes.private_messages_system import pm_system_blueprint
    from .routes.notifications import notifications_blueprint

    app.register_blueprint(user_profile_blueprint)
    app.register_blueprint(forget_password_blueprint)
    app.register_blueprint(populary_posts_blueprint)
    app.register_blueprint(follows_blueprint)
    app.register_blueprint(settings_blueprint)
    app.register_blueprint(editsystem_blueprint)
    app.register_blueprint(likesystem_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(remove_blueprint)
    app.register_blueprint(add_post_blueprint)
    app.register_blueprint(add_comment_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(logout_blueprint)
    app.register_blueprint(remove_comment_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(pm_system_blueprint)
    app.register_blueprint(notifications_blueprint)

    return app
