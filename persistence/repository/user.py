from persistence import fetchall, fetchone, execute
from persistence.model.user import User


class UserRepository:
    @staticmethod
    def find_all():
        query = '''
                SELECT `id`, `username`, `password`, `role`
                FROM `users`
                ORDER BY `role`, `username`;
        '''

        return [User.create_from_data(data) for data in fetchall(query)]

    @staticmethod
    def find_by_id(user_id):
        query = '''
                SELECT `id`, `username`, `password`, `role`
                FROM `users`
                WHERE `id` = %s;
        '''
        args = (user_id,)

        return User.create_from_data(fetchone(query, args))

    @staticmethod
    def find_by_username(username):
        query = '''
                SELECT `id`, `username`, `password`, `role`
                FROM `users`
                WHERE `username` = %s;
        '''
        args = (username,)

        return User.create_from_data(fetchone(query, args))

    @staticmethod
    def save(user):
        if user.user_id is None:
            query = '''
                    INSERT INTO `users`
                        (`username`, `password`, `role`)
                    VALUES(%s, %s, %s);
            '''
            args = (user.username, user.digest, user.role)
            user.user_id = execute(query, args)
        else:
            query = '''
                    UPDATE `users`
                    SET `username` = %s,
                        `password` = %s,
                        `role` = %s
                    WHERE `id` = %s;
            '''
            args = (user.username, user.digest, user.role, user.user_id)
            execute(query, args)

        return user

    @staticmethod
    def delete_by_id(user_id):
        query = '''
                DELETE FROM `users`
                WHERE `id` = %s;
        '''
        args = (user_id,)
        execute(query, args)
