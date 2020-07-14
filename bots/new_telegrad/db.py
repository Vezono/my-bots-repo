import random

from pymongo import MongoClient

from config import environ


class Database:
    def __init__(self):
        client = MongoClient(environ['database'])
        self.users = client.telegrad.users
        self.locs = client.telegrad.locs
        self.kvs = client.telegrad.kvs
        self.cache = {
            'newbies': {}
        }

    def get_user(self, user_id):
        return self.users.find_one({'id': user_id})

    def form_user_dict(self, user):
        commit = {
            'id': user.id,
            'name': user.first_name.split(' ')[0],
            'gender': random.choice(['male', 'female']),
            'age': random.randint(18, 25),
            'money': random.randint(2000, 2500),
            'inv': [],
            'stats': {
                'hunger': 100,
                'maxhunger': 100,

                'health': 100,
                'maxhealth': 100,

                'power': 40,
                'maxpower': 100,

                'sleep': 100,
                'maxsleep': 100,

                'strenght': 50,
                'intelligence': 50,
            },
            'body': {
                'hair': {
                    'color': random.choice(['light', 'gold', 'black', 'chestnut']),
                    'lenght': random.choice(['short', 'middle', 'long']),
                },
                'height': random.randint(150, 190)
            }
        }
        self.cache.update({'newbies': {user.id: commit}})
        return commit

    def user_ever_been(self, user_id):
        return user_id in self.cache['newbies'] or self.get_user(user_id)


db = Database()
