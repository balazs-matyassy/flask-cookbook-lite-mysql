from persistence import fetchall, fetchone, execute
from persistence.model.recipe import Recipe


class RecipeRepository:
    @staticmethod
    def find_all():
        query = '''
                SELECT `id`, `category`,`name`, `description`, `difficulty`
                FROM `recipes`
                ORDER BY `category`, `name`;
        '''

        return [Recipe.create_from_data(data) for data in fetchall(query)]

    @staticmethod
    def find_by_id(recipe_id):
        query = '''
                SELECT `id`, `category`, `name`, `description`, `difficulty`
                FROM `recipes`
                WHERE `id` = %s;
        '''
        args = (recipe_id,)

        return Recipe.create_from_data(fetchone(query, args))

    @staticmethod
    def find_by_name(name):
        query = '''
                SELECT `id`, `category`, `name`, `description`, `difficulty`
                FROM `recipes`
                WHERE `name` LIKE %s
                ORDER BY `category`, `name`;
        '''
        args = (f'%{name}%',)

        return [Recipe.create_from_data(data) for data in fetchall(query, args)]

    @staticmethod
    def save(recipe):
        if recipe.recipe_id is None:
            query = '''
                    INSERT INTO `recipes`
                        (`category`, `name`, `description`, `difficulty`)
                    VALUES(%s, %s, %s, %s);
            '''
            args = (
                recipe.category,
                recipe.name,
                recipe.description,
                recipe.difficulty
            )
            recipe.recipe_id = execute(query, args)
        else:
            query = '''
                    UPDATE `recipes`
                    SET `category` = %s,
                        `name` = %s,
                        `description` = %s,
                        `difficulty` = %s
                    WHERE `id` = %s;
            '''
            args = (
                recipe.category,
                recipe.name,
                recipe.description,
                recipe.difficulty,
                recipe.recipe_id
            )
            execute(query, args)

        return recipe

    @staticmethod
    def delete_by_id(recipe_id):
        query = '''
                DELETE FROM `recipes`
                WHERE `id` = %s;
        '''
        args = (recipe_id,)
        execute(query, args)
