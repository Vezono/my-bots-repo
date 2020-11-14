from pymongo import MongoClient

import config


class Database:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).myvodafone
        self.users = self.db.users

    def get_user(self, user_id):
        return self.db.users.find_one({'id': user_id})

    def create_user(self, user_id, token):
        user = {
            'id': user_id,
            'token': token
        }
        if self.get_user(user_id):
            self.users.update_one({'id': user_id})
        else:
            self.users.insert_one(user)
