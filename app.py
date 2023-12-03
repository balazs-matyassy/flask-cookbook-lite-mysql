from flask import Flask

import blueprints.pages
import blueprints.recipes
import blueprints.security
import blueprints.users
import persistence
import security
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    persistence.init_app(app)
    security.init_app(app)

    app.register_blueprint(blueprints.pages.bp, url_prefix='/')
    app.register_blueprint(blueprints.recipes.bp, url_prefix='/recipes')
    app.register_blueprint(blueprints.security.bp, url_prefix='/')
    app.register_blueprint(blueprints.users.bp, url_prefix='/users')

    return app


if __name__ == '__main__':
    create_app().run()
