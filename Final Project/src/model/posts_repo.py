from src.model.repo import PostgresRepo
from src.model.models import Post
import uuid
import datetime

class PostsRepo(PostgresRepo):

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
            posts_data = cur.fetchall()
            posts = [Post.from_db(post).__dict__ for post in posts_data]
            cur.close()
            conn.close()

            return posts
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

    def get_pet_posts(self, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT id, pet_id, message, photo, post_date FROM posts WHERE pet_id = %s', (pet_id,))
            posts_data = cur.fetchall()
            posts = [Post.from_db(post).__dict__ for post in posts_data]
            cur.close()
            conn.close()
            return posts
        except Exception as e:
            print(e)

    def delete_post(self, post_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
        conn.commit()
        cur.close()
        conn.close()
        return post_id