from flask import Blueprint

bp = Blueprint('recipes', __name__)

from blueprints.recipes import routes
