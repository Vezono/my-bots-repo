import random

from pymongo import MongoClient

import config


class Database:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).free_telegrad
        self.users = self.db.users
        self.sync_db()

    def get_user(self, user_id):
        return self.db.users.find_one({'id': user_id})

    def create_user(self, user_id, preset=None):
        if preset is None:
            preset = {}
        user = self.form_newbie(user_id)
        user.update(preset)
        if self.get_user(user_id):
            self.users.update_one({'id': user_id}, user)
        else:
            self.users.insert_one(user)

    def proceed_user(self, user_id, name):
        if not self.get_user(user_id):
            self.create_user(user_id)
        self.users.update_one({'id': user_id}, {'$set': {'name': name}})
        return self.get_user(user_id)

    def inc_stat(self, user_id, stat, value):
        self.users.update_one({'id': user_id}, {'$inc': {stat: value}})

    def set_stat(self, user_id, stat, value):
        self.users.update_one({'id': user_id}, {'$set': {stat: value}})

    def get_users(self):
        return self.db.users.find({})

    def form_newbie(self, user_id):
        return {
            'id': user_id,
            'name': None,
            'age': None,
            'money': random.randint(2500, 5000)
        }

    def sync_db(self):
        for user in self.users.find({}):
            new_user = self.form_newbie(user['id'])
            new_user.update(user)
            self.users.update_one({'id': user['id']}, new_user)

    def wipe_all(self):
        self.users.drop()
