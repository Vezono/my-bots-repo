import random

from pymongo import MongoClient

from config import environ
from .constants import *


class Database:
    def __init__(self):
        client = MongoClient(environ['egor_database'])
        self.users = client.lifesim.users
        self.locs = client.lifesim.locs
        self.kvs = client.lifesim.kvs
        self.all_users({'human.walking': False})
        for street in streets:
            street = streets[street]
            if not self.get_street(street['code']):
                self.locs.insert_one(street)
        for street in self.locs.find({}):
            for building in street['buildings']:
                building = street['buildings'][building]
                if building['type'] == 'shop':
                    for product in streets[street['code']]['buildings'][building['code']]['products']:
                        product = streets[street['code']]['buildings'][building['code']]['products'][product]
                        if product['code'] not in building['products']:
                            self.locs.update_one({'code': street['code']},
                                                 {'$set': {
                                                     f'buildings.{building["code"]}.products.{product["code"]}': product}})

    def all_users(self, query, method='set', docs=None):
        if docs is None:
            docs = {}
        self.users.update_many(docs, {f'${method}': query})

    def all_kvs(self, query, method='set', docs=None):
        if docs is None:
            docs = {}
        self.kvs.update_many(docs, {f'${method}': query})

    def all_locs(self, query, method='set', docs=None):
        if docs is None:
            docs = {}
        self.locs.update_many(docs, {f'${method}': query})

    def get_user(self, user):
        user = self.users.find_one({'id': user.id})
        if not user:
            self.users.insert_one(createuser(user))
            user = self.users.find_one({'id': user.id})
            hom = user['human']['home']
            street = user['human']['street']
            self.kvs.insert_one(createkv(user, hom, street))
        return user

    def get_street(self, code):
        return self.locs.find_one({'code': code})

    def clear_all(self):
        self.users.remove({})
        self.kvs.remove({})

    def get_friend(self, name):
        self.users.find_one({'human.name': name})

    def get_kv(self, h):
        self.kvs.find_one({'id': h['position']['flat']})

    def unlock_kv(self, kv):
        self.kvs.update_one({'id': kv['id']}, {'$set': {'locked': False}})

    def lock_kv(self, kv):
        self.kvs.update_one({'id': kv['id']}, {'$set': {'locked': True}})


def createuser(user):
    return {
        'id': user.id,
        'name': user.first_name,
        'username': user.username,
        'human': human(user),
        'newbie': True,
        'start_stats': True,
        'wait_for_stat': None
    }


def createkv(user, hom, street):
    return {
        'id': user.id,
        'name': user.first_name,
        'home': hom,
        'street': street,
        'locked': True,
        'objects': {
            'fridge': {
                'maxweight': 500,
                'inv': [],
                'money_hour': 1,
                'type': 'fridge',
                'code': 'fridge'
            }
        },
        'humans': []
    }


def human(user):
    allstrs = []
    for ids in streets:
        if len(streets[ids]['homes']) > 0:
            allstrs.append(streets[ids])
    street = random.choice(allstrs)
    home = random.choice(street['homes'])
    key = street['code'] + '#' + home + '#' + str(user.id)
    return {
        'name': None,
        'gender': random.choice(['male', 'female']),
        'age': random.randint(18, 25),
        'money': random.randint(2000, 2500),
        'street': street['code'],
        'home': home,
        'keys': [key],
        'position': {
            'street': 'meet_street',
            'flat': None,
            'building': None
        },
        'hunger': 100,
        'maxhunger': 100,
        'health': 100,
        'maxhealth': 100,
        'strenght': random.randint(3, 3),
        'intelligence': random.randint(3, 3),
        'power': 40,
        'maxpower': 100,
        'sleep': 100,
        'maxsleep': 100,
        'education': 'basic',
        'mix': [],
        'take_away': False,
        'walking': False,
        'inv': [],
        'inv_maxweight': 50,
        'shop_inv': [],
        'kl': True,
        'br': False,
        'body': {
            'hair_color': random.choice(h_colors),
            'hair_lenght': random.choice(h_lenghts),
            'height': random.randint(150, 190)
        }

    }
