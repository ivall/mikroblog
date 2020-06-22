from flask import redirect, url_for, flash, jsonify, request


def page_not_found(e):
    return redirect(url_for('index_blueprint.index'))


def method_not_allowed(e):
    return jsonify('Metoda niedozwolona')


def request_entity_too_large(e):
    flash("Maksymalna wielkość pliku wynosi 1MB.")
    return redirect(url_for('index_blueprint.index'))


def ratelimit_handler(e):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.accept_mimetypes.accept_json:
        return jsonify({'information': 'Zwolnij trochę ;)'}), 409
    flash(f"Zwolnij trochę ;)")
    return redirect(url_for('index_blueprint.index'))