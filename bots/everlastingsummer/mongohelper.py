from pymongo import MongoClient

from . import config
from .pioner import Pioner


class MongoHelper:
    def __init__(self):
        self.client = MongoClient(config.environ['es_database'])
        self.db = self.client.new_everlastingsummer

    def get_pioners(self):
        pioners = self.db.users.find({})
        return [Pioner(
            pioner['id'], pioner['gender'], pioner['name'], pioner['strength'],
            pioner['agility'], pioner['intelligence'], pioner['respects']
        ) for pioner in pioners if not self.user_banned(pioner['id'])]

    def get_pioner(self, user_id):
        pioner = self.db.users.find_one({'id': user_id})
        if not pioner:
            return
        return Pioner(
            pioner['id'], pioner['gender'], pioner['name'], pioner['strength'],
            pioner['agility'], pioner['intelligence'], pioner['respects']
        )

    def create_pioner(self, user, name, gender):
        commit = {
            'id': user.id,
            'gender': gender,
            'name': name,
            'strength': 3,
            'agility': 3,
            'intelligence': 3,
            'respects': {
                pioner: 50 for pioner in config.pioners
            }
        }
        self.db.users.insert_one(commit)

    def increase_value(self, user_id, params):
        self.db.users.update_one({'id': user_id}, {'$inc': params})

    def user_banned(self, user_id):
        return self.db.banned.find_one({'id': user_id})

    def get_bot_admins(self, pioner):
        admins = [user.id for user in self.db.admins.find({pioner: True})] + config.admins
        return admins

    def add_bot_admin(self, pioner, user_id):
        commit = {}
        if not self.db.admins.find_one({'id': user_id}):
            commit = {bot[:3]: False for bot in config.pioners}
        commit.update({pioner: True})
        self.db.admins.update_one({'id': user_id}, {'$set': commit})

    def del_bot_admin(self, pioner, user_id):
        commit = {}
        if not self.db.admins.find_one({'id': user_id}):
            commit = {bot[:3]: False for bot in config.pioners}
        commit.update({pioner: False})
        self.db.admins.update_one({'id': user_id}, {'$set': commit})
