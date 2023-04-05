import os
import psycopg2
import datetime
import uuid

class PostgresRepo:
    def __init__(self):
        self.host = os.environ['POSTGRES_HOST']
        self.database = os.environ['POSTGRES_DATABASE']
        self.username = os.environ['POSTGRES_USERNAME']
        self.password = os.environ['POSTGRES_PASSWORD']

    def get_conn(self):
        return psycopg2.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password= self.password)

    """
    TODO: Here are other methods that need to be defined for the app

    def get_users():
    def delete_user(user_id):

    def get_pet(pet_id):
    def get_pets(user_id):
    def get_pets_by_species(species):
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

