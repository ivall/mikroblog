from flask import redirect, url_for, flash

def page_not_found(e):
    flash("404, nie znaleziono strony")
    return redirect(url_for('index'))
