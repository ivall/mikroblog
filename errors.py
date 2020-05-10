from flask import redirect, url_for, flash

def page_not_found(e):
    return redirect(url_for('index'))

def method_not_allowed(e):
    return "<h1>Wystąpił błąd 405 - metoda niedozwolona</h1>"