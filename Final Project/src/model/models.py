import uuid
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

class Pet(object):
    def __init__(self, id, user_id, name, nicknames, species, breed, profile_pic, birthday, gender, is_active, photos):
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
        self.photos = photos

    @staticmethod
    def from_db(record):
        return Pet(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10])

    @staticmethod
    def from_dict(dict):
        pet_id = None
        if 'id' in dict:
            pet_id = dict['id']
        else:
            pet_id = str(uuid.uuid4())
        return Pet(
            pet_id,
            dict['user_id'],
            dict['name'],
            dict['nicknames'],
            dict['species'],
            dict['breed'],
            dict['profile_pic'],
            dict['birthday'],
            dict['gender'],
            dict['is_active'],
            dict['photos'])


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

    @staticmethod
    def from_dict(dict):
        post_id = None
        if 'id' in dict:
            post_id = dict['id']
        else:
            post_id= str(uuid.uuid4())
        return Post(
            post_id,
            dict['pet_id'],
            dict['message'],
            dict['photo'],
            dict['post_date'])

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