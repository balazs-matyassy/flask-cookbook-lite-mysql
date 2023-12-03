from flask import request


class EntityForm:
    def __init__(self, entity):
        self.entity = entity
        self.errors = []

    @property
    def create_form(self):
        return self.entity.entity_id is None

    def validate_on_submit(self):
        if request.method != 'POST':
            return False

        self.entity.update(request.form)
        self.errors = self.entity.validate()

        return len(self.errors) == 0
