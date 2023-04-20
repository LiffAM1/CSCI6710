from model.repo import PostgresRepo
from model.models import Reaction

class ReactionsRepo(PostgresRepo):

    def get_post_reactions(self, post_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT r.id, r.post_id, r.pet_id, r.type, r.message FROM reactions r '
                        'WHERE r.post_id = %s', (post_id,))
            reactions_data = cur.fetchall()
            reactions = [Reaction.from_db(
                reaction).__dict__ for reaction in reactions_data]
            cur.close()
            conn.close()

            return reactions
        except Exception as e:
            print(e)

    def get_post_treats(self, post_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT r.id, r.post_id, r.pet_id, r.type, r.message FROM reactions r '
                        'WHERE r.post_id = %s AND r.type = 1', (post_id,))
            reactions_data = cur.fetchall()
            reactions = [Reaction.from_db(
                reaction).__dict__ for reaction in reactions_data]
            cur.close()
            conn.close()

            return reactions
        except Exception as e:
            print(e)

    def get_post_comments(self, post_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT r.id, r.post_id, r.pet_id, r.type, r.message FROM reactions r '
                        'WHERE r.post_id = %s AND r.type = 2', (post_id,))
            reactions_data = cur.fetchall()
            reactions = [Reaction.from_db(
                reaction).__dict__ for reaction in reactions_data]
            cur.close()
            conn.close()

            return reactions
        except Exception as e:
            print(e)

    def create_post_reaction(self, reaction):
        try:
            treat = self.get_treat_by_petid(reaction.post_id, reaction.pet_id)
            if treat != None and reaction.type == 1:
                raise Exception("Treat already given.")
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('INSERT INTO reactions (id, post_id, pet_id, type, message) '
                        'VALUES (%s,%s,%s,%s,%s)',
                        (reaction.id, reaction.post_id, reaction.pet_id, reaction.type, reaction.message,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def get_treat_by_petid(self, post_id, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT r.id, r.post_id, r.pet_id, r.type, r.message FROM reactions r '
                        'WHERE r.post_id = %s AND r.pet_id = %s AND r.type = 1', (post_id, pet_id,))
            treat = cur.fetchone()

            cur.close()
            conn.close()

            if treat:
                return Reaction.from_db(treat).__dict__
            return None
        except Exception as e:
            print(e)

    def delete_post_reaction(self, reaction_id):
        try:
            existing = self.get_reaction(reaction_id)
            if not existing:
                return None

            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('DELETE FROM reactions WHERE id = %s', (reaction_id,))
            conn.commit()
            cur.close()
            conn.close()

            return reaction_id
        except Exception as e:
            print(e)

    def get_reaction(self, reaction_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT r.id, r.post_id, r.pet_id, r.type, r.message FROM reactions r '
                        'WHERE r.id = %s', (reaction_id,))
            reaction = cur.fetchone()

            cur.close()
            conn.close()

            if reaction:
                return Reaction.from_db(reaction).__dict__
            return None
        except Exception as e:
            print(e)
