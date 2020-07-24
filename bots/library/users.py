import typing
from pymongo import MongoClient
import config
db = MongoClient(config.environ['database']).library

import dataclass_factory

from .user import User


class Users:
    def __init__(self):
        self.factory = dataclass_factory.Factory()
        self.sync_all_users()

    @property
    def all_users(self) -> typing.List[User]:
        users = db.users.find({})
        return [self.deserialize_user(user) for user in users]

    def sync_user(self, user: User):
        sample_user_dict = self.form_user_dict(user.id, user.name)
        user_dict = self.serialize_user(user)
        for line in sample_user_dict:
            if line not in user_dict:
                user_dict.update({line: sample_user_dict[line]})
        self.update_user(user.id, user_dict)

    def sync_all_users(self):
        for user in self.all_users:
            self.sync_user(user)

    def sync_tg_user(self, tg_user):
        user = self.get_user(tg_user.id)
        if not user:
            return self.create_user(tg_user)
        sample_user_dict = self.form_user_dict(tg_user.id, tg_user.first_name)
        user_dict = self.serialize_user(user)
        for line in sample_user_dict:
            if line not in user_dict:
                user_dict.update({line: sample_user_dict[line]})
        self.update_user(tg_user.id, user_dict)

    def get_user(self, user_id):
        user = db.users.find_one({'id': user_id})
        if not user:
            return None
        return self.deserialize_user(user)

    def get_user_dict(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return None
        return self.serialize_user(user)

    def deserialize_user(self, user) -> User:
        return self.factory.load(user, User)

    def serialize_user(self, user: User) -> dict:
        return self.factory.dump(user)

    def create_user(self, tg_user):
        user = self.form_user_dict(tg_user.id, tg_user.first_name)
        db.users.insert_one(user)
        return self.deserialize_user(user)

    @staticmethod
    def update_user(user_id, param, method='$set'):
        db.users.update_one({'id': user_id}, {method: param})

    @staticmethod
    def form_user_dict(user_id, name):
        return {
            'id': user_id,
            'name': name.split(' ')[0],
            'readed': [],
            'pushed': [],
            'points': 0
        }
