from src.model.repo import PostgresRepo
from src.model.models import Pet 

class PetsRepo(PostgresRepo):

    def get_pet(self, id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, user_id, name, nicknames, species, breed, profile_pic, birthday, gender, is_active FROM pets WHERE id = %s', (id,))
        pet = cur.fetchone()
        cur.close()
        conn.close()
        if pet:
            return Pet.from_db(pet.__dict__)
        return None

    def get_pets(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, user_id, name, nicknames, species, breed, profile_pic, birthday, gender, is_active FROM pets')
        pets = cur.fetchall()
        cur.close()
        conn.close()
        return [Pet.from_db(pet).__dict__ for pet in pets]

    def get_user_pets(self, user_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT id, user_id, name, nicknames, species, breed, profile_pic, birthday, gender, is_active FROM pets WHERE user_id = %s', (user_id,))
        pets = cur.fetchall()
        cur.close()
        conn.close()
        return [Pet.from_db(p).__dict__ for p in pets]

    def create_pet(self, pet):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO pets (id, user_id, name, nicknames, species, breed, profile_pic, birthday, gender, is_active)'
                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (pet.id, pet.user_id, pet.name, pet.nicknames, pet.species, pet.breed, pet.profile_pic, pet.birthday, pet.gender, pet.is_active))
        conn.commit()
        cur.close()
        conn.close()

    def update_pet(self, pet):
        existing = self.get_pet(pet.id)
        if not existing:
            return None

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('UPDATE pets SET name = %s, nicknames = %s, species = %s, breed = %s, profile_pic = %s, birthday = %s, gender = %s, is_active = %s WHERE id = %s',
                    (pet.name, pet.nicknames, pet.species, pet.breed, pet.profile_pic, pet.birthday, pet.gender, pet.is_active, pet.id))
        conn.commit()
        cur.close()
        conn.close()
        return pet.__dict__

    def set_pet_active(self, pet_id):
        existing = self.get_pet(pet_id)
        if not existing:
            return None

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('UPDATE pets SET is_active = TRUE WHERE id = %s', (pet_id,))
        conn.commit()
        cur.close()
        conn.close()
        return self.get_pet(pet_id)

    def set_pet_inactive(self, pet_id):
        existing = self.get_pet(pet_id)
        if not existing:
            return None

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('UPDATE pets SET is_active = FALSE WHERE id = %s', (pet_id,))
        conn.commit()
        cur.close()
        return self.get_pet(pet_id)

    def delete_pet(self, pet_id):
        existing = self.get_pet(pet_id)
        if not existing:
            return None

        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM pets WHERE id = %s', (pet_id,))
        conn.commit()
        cur.close()
        conn.close()
        return pet_id