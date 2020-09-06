from pymongo import MongoClient
import config


class Database:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).mystat.users

    def get_user(self, user_id):
        return self.db.find_one({'id': user_id})

    def login(self, **kwargs):
        user = self.db.find_one(kwargs)
        if not user:
            self.db.insert_one(kwargs)


db = Database()
