from flask import session, url_for, redirect
from flask import Blueprint


logout_blueprint = Blueprint('logout_blueprint', __name__)


@logout_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index_blueprint.index'))
