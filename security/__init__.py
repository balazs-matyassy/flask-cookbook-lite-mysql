from flask import g, session

from persistence.repository.user import UserRepository


def init_app(app):
    app.before_request(__load_current_user)
    app.jinja_env.globals['is_fully_authenticated'] = lambda: g.user
    app.jinja_env.globals['has_admin_role'] = lambda: g.user and g.user.admin


def __load_current_user():
    if session.get('user_id') is None:
        g.user = None
    else:
        g.user = UserRepository.find_by_id(session.get('user_id'))
