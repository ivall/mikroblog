from flask import redirect, url_for, flash

def page_not_found(e):
    return redirect(url_for('index'))
