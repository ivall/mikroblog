from flask import Flask



def create_app():
    from .errors import page_not_found
    from .errors import method_not_allowed
    app = Flask(__name__)
    app.config.from_object('config')

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    from .blueprints.logout import logout_blueprint
    from .blueprints.register import register_blueprint
    from .blueprints.login import login_blueprint
    from .blueprints.add_comment import add_comment_blueprint
    from .blueprints.add_post import add_post_blueprint
    from .blueprints.remove import remove_blueprint
    from .blueprints.post import post_blueprint
    from .blueprints.remove_comment import remove_comment_blueprint
    from .blueprints.likesystem import likesystem_blueprint
    from .blueprints.editsystem import editsystem_blueprint
    from .blueprints.settings import settings_blueprint
    from .blueprints.follows import follows_blueprint
    from .blueprints.populary_posts import populary_posts_blueprint
    from .blueprints.forget_password import forget_password_blueprint
    from .blueprints.user_profile import user_profile_blueprint
    from .blueprints.index import index_blueprint
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

    return app
