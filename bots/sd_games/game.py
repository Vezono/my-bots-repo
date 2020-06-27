import random

from pymongo import MongoClient

import config

client = MongoClient(config.environ['database'])
db = client.collect_goats


class Game:
    def __init__(self, size=11):
        self.icons = {
            'wall': '⬛️',
            'goat': '🐐',
            'nothing': 'ᅠ'
        }
        self.size = size
        self.players = dict()
        self.map = dict()
        self.spawns = ['5_5']

        self.db_map = db.map
        self.db_users = db.users

        self.up_data()

    def get_near(self, pos):
        x = int(pos.split("_")[0])
        y = int(pos.split("_")[1])
        near = []
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                tile = f'{x + i}_{y + j}'
                if self.map.get(tile) != 'wall':
                    near.append(tile)
        return near

    @staticmethod
    def get_map(pos) -> list:
        x = int(pos.split("_")[0])
        y = int(pos.split("_")[1])
        near = []
        for j in [-2, -1, 0, 1, 2]:
            for i in [-2, -1, 0, 1, 2]:
                near.append(f'{x + i}_{y + j}')
        return near

    def get_icon(self, pos) -> str:
        player_poss = [self.players[player]['icon'] for player in self.players if self.players[player]['pos'] == pos]
        if player_poss:
            return player_poss[0]
        tile = self.map.get(pos)
        if not tile:
            self.map.update({pos: random.choice(list(self.icons.keys()))})
        tile = self.map.get(pos)
        return self.icons[tile]

    def create_player(self, user):
        pos = random.choice(self.spawns)
        commit = {
            'id': user.id,
            'name': user.first_name,
            'pos': pos,
            'icon': '🔵',
            'goats': 0
        }
        self.players.update({
            str(user.id): commit
        })

    def up_data(self):
        self.players = self.db_users.find_one({})
        del self.players["_id"]
        self.map = self.db_map.find_one({})
        del self.map["_id"]

    def down_data(self):
        map = self.db_map.find_one({})
        if not map:
            self.db_map.insert_one(self.map)
        else:
            self.db_map.update_one({}, {'$set': self.map})
        players = self.db_users.find_one({})
        if not players:
            self.db_users.insert_one(self.players)
        else:
            self.db_users.update_one({}, {'$set': self.players})
        self.up_data()
