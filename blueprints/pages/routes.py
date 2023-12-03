from flask import render_template

from blueprints.pages import bp


@bp.route('/')
def home():
    return render_template('pages/home.html')
