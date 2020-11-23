from pymongo import MongoClient

import config


class Database:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).slavya
        self.users = self.db.users

    def get_user(self, user_id):
        return self.db.users.find_one({'id': user_id})

    def create_user(self, user_id):
        user = {
            'id': user_id,
            'rep': 0,
            'pancakes': 0,
            'cooked': 0,
            'been_cooked': 0,
            'throwed': 0,
            'been_throwed': 0
        }
        if self.get_user(user_id):
            self.users.update_one({'id': user_id})
        else:
            self.users.insert_one(user)

    def proceed_user(self, user_id):
        if not self.get_user(user_id):
            self.create_user(user_id)
        return self.get_user(user_id)

    def inc_stat(self, user_id, stat, value):
        self.users.update_one({'id': user_id}, {'$inc': {stat: value}})

    def set_stat(self, user_id, stat, value):
        self.users.update_one({'id': user_id}, {'$set': {stat: value}})
