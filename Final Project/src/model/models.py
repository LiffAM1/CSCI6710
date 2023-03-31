class User:
    def __init__(self, id, name, email, is_active, is_authenticated):
        self.id = id
        self.name = name
        self.email = email
        self.is_active = is_active
        self.is_authenticated = is_authenticated

    def get_id(self):
        return self.id

    @staticmethod
    def from_db(record):
        return User(record[0],record[1],record[2],record[3],record[4])

class Pet:
    def __init__(self, id, user_id, name, nicknames, species, breed, profile_pic, birthday, gender, is_active):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.nicknames = nicknames
        self.species = species
        self.breed = breed
        self.profile_pic = profile_pic
        self.birthday = birthday
        self.gender = gender
        self.is_active = is_active 

    @staticmethod
    def from_db(record):
        return Pet(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9])

class Friend:
    def __init__(self, id, pet_id, friend_id, friend_date):
        self.id = id
        self.pet_id = pet_id
        self.friend_id = friend_id
        self.friend_date = friend_date

    @staticmethod
    def from_db(record):
        return Friend(record[0],record[1],record[2],record[3])

class Post:
    def __init__(self, id, pet_id, message, photo, post_date):
        self.id = id
        self.pet_id = pet_id
        self.message = message
        self.photo = photo 
        self.post_date = post_date

    @staticmethod
    def from_db(record):
        return Post(record[0],record[1],record[2],record[3],record[4])

class Reaction:
    def __init__(self, id, post_id, pet_id, type, message):
        self.id = id
        self.post_id = post_id 
        self.pet_id = pet_id
        self.type = type
        self.message = message

    @staticmethod
    def from_db(record):
        return Reaction(record[0],record[1],record[2],record[3],record[4])