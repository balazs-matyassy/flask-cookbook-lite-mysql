import click
import pymysql
import pymysql.cursors
from flask import g, current_app
from pymysql.constants import CLIENT
from werkzeug.security import generate_password_hash


def init_app(app):
    app.cli.add_command(__install_command)
    app.cli.add_command(__reset_admin_command)
    app.before_request(__on_before_request)
    app.teardown_appcontext(__on_teardown_appcontext)


def get_connection(multi_statements=False):
    client_flag = CLIENT.MULTI_STATEMENTS if multi_statements else 0

    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USERNAME'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_DATABASE'],
        cursorclass=pymysql.cursors.DictCursor,
        client_flag=client_flag
    )


def execute(query, args=None, db=None):
    db = db or g.db

    with db.cursor() as cursor:
        cursor.execute(query, args)
        lastrowid = cursor.lastrowid

    db.commit()

    return lastrowid


def fetchone(query, args=None, db=None):
    db = db or g.db

    with db.cursor() as cursor:
        cursor.execute(query, args)

        return cursor.fetchone()


def fetchall(query, args=None, db=None):
    db = db or g.db

    with db.cursor() as cursor:
        cursor.execute(query, args)

        return cursor.fetchall()


def install():
    with get_connection(True) as db:
        with current_app.open_resource('schema.sql') as file:
            execute(file.read().decode('utf8'), db=db)

        __reset_admin(db)


def reset_admin():
    with get_connection() as db:
        __reset_admin(db)


def __reset_admin(db):
    query = '''
            SELECT `id`
            FROM `users`
            WHERE `username` = 'admin';
    '''

    user_id = (fetchone(query, db=db) or {'id': None})['id']
    digest = generate_password_hash('Admin123.')

    if user_id:
        query = '''
                UPDATE `users`
                SET `username` = %s,
                    `password` = %s,
                    `role`     = %s
                WHERE `id` = %s;
        '''
        args = ('admin', digest, 'admin', user_id)
    else:
        query = '''
                INSERT INTO `users`
                    (`username`, `password`, `role`)
                VALUES (%s, %s, %s);
        '''
        args = ('admin', digest, 'admin')

    execute(query, args, db=db)


@click.command('install')
def __install_command():
    install()
    click.echo('Application installation successful.')


@click.command('reset-admin')
def __reset_admin_command():
    reset_admin()
    click.echo('Admin reset successful.')


def __on_before_request():
    if 'db' not in g:
        g.db = get_connection()


def __on_teardown_appcontext(e):
    if 'db' in g:
        g.pop('db').close()


from persistence.model.user import User
from persistence.repository.recipe import RecipeRepository
from persistence.repository.user import UserRepository
