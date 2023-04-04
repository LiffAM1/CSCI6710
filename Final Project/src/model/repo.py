import os
import psycopg2
import datetime
import uuid

from src.model.models import User, Post

class PostgresRepo:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'postgres'
        self.username = os.environ['POSTGRES_USERNAME']
        self.password = os.environ['POSTGRES_PASSWORD']

    def get_conn(self):
        return psycopg2.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password= self.password)

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

    def set_active(self, user_id):
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

    def set_inactive(self, user_id):
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

    """
    TODO: Here are other methods that need to be defined for the app

    def get_users():
    def delete_user(user_id):

    def get_pet(pet_id):
    def get_pets(user_id):
    def get_pets_by_species(species):
    def create_pet(pet):
    def update_pet(pet):
    def delete_pet(pet_id):
    def set_active(pet_id):
    def set_inactive(pet_id):

    def get_friends(pet_id):
    def get_non_friends(pet_id):
    def add_friend(pet_id, friend_id):
    def delete_friend(pet_id, friend_id):
    
    def update_post(post):

    def get_post_reactions(post_id):
    def get_post_treats(post_id):
    def get_post_comments(post_id):
    def create_post_reaction(reaction):
    def delete_post_reaction(reaction_id):
    """

    def create_post(self, petId, message):
        try:
            currentDate = datetime.datetime.now()
            id = str(uuid.uuid4())

            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('INSERT INTO posts (id, pet_id, message, photo, post_date)'
                        'VALUES (%s,%s,%s,%s,%s)',
                        (id, petId, message, "", currentDate))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def get_friend_posts(self, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT p.id, p.pet_id, p.message, p.photo, p.post_date FROM posts p JOIN friends f on f.friend_id = p.pet_id WHERE f.pet_id = %s ORDER BY p.post_date DESC LIMIT 10', (pet_id,))

            posts = []
            for post in cur:
                posts.append(Post.from_db(post).__dict__)

            cur.close()
            conn.close()

            if len(posts) > 0:
                return posts
            return None
        except Exception as e:
            print(e)

    def get_post(self, post_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT id, pet_id, message, photo, post_date FROM posts WHERE id = %s', (post_id,))
            post = cur.fetchone()

            cur.close()
            conn.close()

            if post:
                return Post.from_db(post).__dict__
            return None
        except Exception as e:
            print(e)

    def get_posts(self, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT id, pet_id, message, photo, post_date FROM posts WHERE pet_id = %s', (pet_id,))

            posts = []
            for post in cur:
                posts.append(Post.from_db(post).__dict__)

            cur.close()
            conn.close()

            if len(posts) > 0:
                return posts
            return None
        except Exception as e:
            print(e)

    def delete_post(self, post_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))

            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)