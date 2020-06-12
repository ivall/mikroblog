from flask import redirect, url_for

def page_not_found(e):
    return redirect(url_for('index_blueprint.index'))

def method_not_allowed(e):
    return "<h1>Wystąpił błąd 405 - metoda niedozwolona</h1>"