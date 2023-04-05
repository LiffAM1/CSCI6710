from src.model.repo import PostgresRepo
from src.model.models import Friend

class FriendsRepo(PostgresRepo):
    def get_friends(self, pet_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute('SELECT id, pet_id, friend_id, friend_date FROM friends WHERE pet_id = %s', (pet_id,))

            friends = []
            for friend in cur:
                friends.append(Friend.from_db(friend).__dict__)

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
            cur.execute('SELECT id, pet_id, friend_id, friend_date FROM friends WHERE pet_id != %s', (pet_id,))

            nonfriends = []
            for nonfriend in cur:
                nonfriends.append(Friend.from_db(nonfriend).__dict__)

            cur.close()
            conn.close()

            if len(nonfriends) > 0:
                return nonfriends
            return None
        except Exception as e:
            print(e)
