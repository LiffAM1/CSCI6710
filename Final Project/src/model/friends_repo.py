from src.model.repo import PostgresRepo
from src.model.models import Pet

class FriendsRepo(PostgresRepo):
    def get_friends(self, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT p.id, p.user_id, p.name, p.nicknames, p.species, p.breed, p.profile_pic, p.birthday, p.gender, p.is_active FROM pets p JOIN friends f ON p.id = f.friend_id WHERE f.pet_id = %s', (pet_id,))

            friends = []
            for friend in cur:
                friends.append(Pet.from_db(friend).__dict__)

            cur.close()
            conn.close()

            if len(friends) > 0:
                return friends
            return None
        except Exception as e:
            print(e)

    def get_non_friends(self, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT p.id, p.user_id, p.name, p.nicknames, p.species, p.breed, p.profile_pic, p.birthday, p.gender, p.is_active ' + 
                        'FROM pets p ' + 
                        'WHERE p.id != %s AND p.id NOT IN (SELECT friend_id FROM friends WHERE pet_id = %s)', (pet_id, pet_id,))

            nonfriends = []
            for nonfriend in cur:
                nonfriends.append(Pet.from_db(nonfriend).__dict__)

            cur.close()
            conn.close()

            if len(nonfriends) > 0:
                return nonfriends
            return None
        except Exception as e:
            print(e)

    def add_friend(self, friend):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('INSERT INTO friends (id, pet_id, friend_id, friend_date)'
                        'VALUES (%s,%s,%s,%s)',
                        (friend.id, friend.pet_id, friend.friend_id, friend.friend_date))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)

    def delete_friend(self, id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('DELETE FROM friends WHERE id = %s', (id,))
            conn.commit()
            cur.close()
            conn.close()

            return id
        except Exception as e:
            print(e)
