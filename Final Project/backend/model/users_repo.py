from model.repo import PostgresRepo
from model.models import User 

class UsersRepo(PostgresRepo):
    def get_user(self, id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT id, name, email, is_active, is_authenticated FROM users WHERE id = %s', (id,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user:
                return User.from_db(user)
            return None
        except Exception as e:
            print(e)

    def create_user(self, user):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('INSERT INTO users (id, name, email, is_active, is_authenticated)'
                        'VALUES (%s,%s,%s,%s,%s)',
                        (user.id, user.name, user.email, user.is_active, user.is_authenticated))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def update_user(self, user):
        try:
            existing = self.get_user(user.id)
            if not existing:
                raise Exception("User not found.")

            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('UPDATE users SET name = %s, email = %s, is_active = %s, is_authenticated = %s WHERE id = %s'
                        (user.name, user.email, user.is_active, user.is_authenticated, user.id))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def set_user_active(self, user_id):
        try:
            existing = self.get_user(user_id)
            if not existing:
                raise Exception("User not found.")

            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('UPDATE users SET is_active = TRUE, is_authenticated = TRUE WHERE id = %s', (user_id,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def set_user_inactive(self, user_id):
        try:
            existing = self.get_user(user_id)
            if not existing:
                raise Exception("User not found.")

            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('UPDATE users SET is_active = FALSE, is_authenticated = FALSE WHERE id = %s', (user_id,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)
