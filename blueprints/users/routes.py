
from flask import render_template, abort, flash, redirect, url_for

from persistence.model.user import User
from persistence.repository.user import UserRepository
from blueprints.forms import EntityForm
from blueprints.users import bp
from security.decorators import is_fully_authenticated, has_admin_role


@bp.route('/')
@is_fully_authenticated
def list_all():
    return render_template('users/list.html', users=UserRepository.find_all())


@bp.route('/create', methods=('GET', 'POST'))
@has_admin_role
def create():
    user = User()
    form = EntityForm(user)

    if form.validate_on_submit():
        try:
            UserRepository.save(user)
            flash('User created.')

            return redirect(url_for('users.list_all'))
        except Exception as err:
            flash(str(err))

    return render_template('users/form.html', form=form)


@bp.route('/edit/<int:user_id>', methods=('GET', 'POST'))
@has_admin_role
def edit(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)
    form = EntityForm(user)

    if form.validate_on_submit():
        try:
            UserRepository.save(user)
            flash('User saved.')

            return redirect(url_for('users.edit', user_id=user.user_id))
        except Exception as err:
            flash(str(err))

    return render_template('users/form.html', form=form)


@bp.route('/delete/<int:user_id>', methods=('POST',))
@has_admin_role
def delete(user_id):
    UserRepository.find_by_id(user_id) or abort(404)

    try:
        UserRepository.delete_by_id(user_id)
        flash('User deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('users.list_all'))
