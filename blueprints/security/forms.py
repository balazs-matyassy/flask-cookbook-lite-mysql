from flask import request


class LoginForm:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.errors = []

    def validate_on_submit(self):
        if request.method != 'POST':
            return False

        self.username = request.form.get('username', '').strip()
        self.password = request.form.get('password', '')
        self.errors = []

        if self.username == '':
            self.errors.append('Username missing.')

        if self.password == '':
            self.errors.append('Password missing.')

        return len(self.errors) == 0
