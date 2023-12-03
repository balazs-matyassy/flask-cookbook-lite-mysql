import base64


class Recipe:
    def __init__(self, category='', name='', description='', difficulty=1, recipe_id=None):
        self.recipe_id = recipe_id
        self.category = category
        self.name = name
        self.description = description
        self.difficulty = difficulty

    @property
    def entity_id(self):
        return self.recipe_id

    @property
    def difficulty_description(self):
        if self.difficulty == 1:
            return 'Very easy'
        elif self.difficulty == 2:
            return 'Easy'
        elif self.difficulty == 3:
            return 'Medium'
        elif self.difficulty == 4:
            return 'Difficult'
        elif self.difficulty == 5:
            return 'Very difficult'

        return 'Unknown'

    def update(self, data):
        self.category = (data.get('category') or '').strip().capitalize()
        self.name = (data.get('name') or '').strip().capitalize()
        self.description = (data.get('description') or '').strip()

        try:
            self.difficulty = int(data.get('difficulty') or 1)

            if self.difficulty < 1:
                self.difficulty = 1
            elif self.difficulty > 5:
                self.difficulty = 5
        except ValueError:
            self.difficulty = 1

    def validate(self):
        errors = []

        if self.category == '':
            errors.append('Category missing.')

        if self.name == '':
            errors.append('Name missing.')

        return errors

    def to_data(self):
        return {
            'id': self.recipe_id,
            'category': self.category,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty
        }

    @staticmethod
    def create_from_data(data):
        if data is None:
            return None

        recipe = Recipe(recipe_id=data['id'])
        recipe.update(data)

        return recipe
