
from flask import request, render_template, abort, flash, redirect, url_for

from persistence.model.recipe import Recipe
from persistence.repository.recipe import RecipeRepository
from blueprints.forms import EntityForm
from blueprints.recipes import bp
from security.decorators import has_admin_role


@bp.route('/')
def list_all():
    if request.args.get('search'):
        recipes = RecipeRepository.find_by_name(request.args.get('search'))
    else:
        recipes = RecipeRepository.find_all()

    return render_template('recipes/list.html', recipes=recipes)


@bp.route('/view/<int:recipe_id>')
def view(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)

    return render_template('recipes/view.html', recipe=recipe)


@bp.route('/create', methods=('GET', 'POST'))
@has_admin_role
def create():
    recipe = Recipe()
    form = EntityForm(recipe)

    if form.validate_on_submit():
        try:
            RecipeRepository.save(recipe)
            flash('Recipe created.')

            return redirect(url_for('recipes.list_all'))
        except Exception as err:
            flash(str(err))

    return render_template('recipes/form.html', form=form)


@bp.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
@has_admin_role
def edit(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    form = EntityForm(recipe)

    if form.validate_on_submit():
        try:
            RecipeRepository.save(recipe)
            flash('Recipe saved.')

            return redirect(url_for('recipes.edit', recipe_id=recipe.recipe_id))
        except Exception as err:
            flash(str(err))

    return render_template('recipes/form.html', form=form)


@bp.route('/delete/<int:recipe_id>', methods=('POST',))
@has_admin_role
def delete(recipe_id):
    RecipeRepository.find_by_id(recipe_id) or abort(404)

    try:
        RecipeRepository.delete_by_id(recipe_id)
        flash('Recipe deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('recipes.list_all'))
