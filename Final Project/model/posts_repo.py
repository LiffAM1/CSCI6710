from model.repo import PostgresRepo
from model.models import Post

class PostsRepo(PostgresRepo):

    def create_post(self, post):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO posts (id, pet_id, message, photo, post_date)'
                    'VALUES (%s,%s,%s,%s,%s)',
                    (post.id, post.pet_id, post.message, post.photo, post.post_date))
        conn.commit()
        cur.close()
        conn.close()

    def get_friend_posts(self, pet_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT p.id, p.pet_id, p.message, p.photo, p.post_date FROM posts p '
                    'JOIN friends f on f.friend_id = p.pet_id '
                    'WHERE f.pet_id = %s ORDER BY p.post_date DESC LIMIT 10', (pet_id,))
        posts_data = cur.fetchall()
        posts = [Post.from_db(post).__dict__ for post in posts_data]
        cur.close()
        conn.close()

        return posts

    def get_post_object(self, post_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, pet_id, message, photo, post_date FROM posts WHERE id = %s', (post_id,))
        post = cur.fetchone()

        cur.close()
        conn.close()

        if post:
            return Post.from_db(post)
        return None

    def get_post(self, post_id):
        return self.get_post_object(post_id).__dict__

    def get_pet_posts(self, pet_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, pet_id, message, photo, post_date FROM posts WHERE pet_id = %s', (pet_id,))
        posts_data = cur.fetchall()
        posts = [Post.from_db(post).__dict__ for post in posts_data]
        cur.close()
        conn.close()
        return posts

    def delete_post(self, post_id):
        existing = self.get_post(post_id)
        if not existing:
            return None

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
        conn.commit()
        cur.close()
        conn.close()
        return post_id