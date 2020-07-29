import random
import typing
from pymongo import MongoClient
import config
import dataclass_factory
from .goat import Goat


class Goats:
    def __init__(self):
        self.db = MongoClient(config.environ['database']).goatwars
        self.goats = self.db.goats
        self.factory = dataclass_factory.Factory()
        self.sync_all_goats()

        self.field = list()

    def ungraze_goats(self, user_id):
        for goat in self.get_user_goats(user_id):
            self.update_goat(goat.id, {'exp': random.randint(1, int(goat.exp * 0.3 + 2))})
            self.field.remove(goat)

    def graze_goats(self, user_id):
        for goat in self.get_user_goats(user_id):
            self.update_goat(goat.id, {'exp': random.randint(1, int(goat.exp * 0.3 + 2))})
            self.field.append(goat)
        if random.randint(1, 100):
            new_holder = random.choice(self.field).holder
            bad_goat = random.choice(self.field)
            bad_goat.holder = new_holder
            self.update_goat(bad_goat.id, {'holder': new_holder})
            self.field.remove(bad_goat)

    def drop_goats(self):
        self.goats.drop()

    @property
    def max_goat_id(self) -> int:
        ids = {goat.id for goat in self.all_goats}
        ids.add(-1)
        return max(ids)

    @property
    def all_goats(self) -> typing.List[Goat]:
        goats = self.goats.find({})
        return [self.deserialize_goat(goat) for goat in goats]

    @property
    def all_goat_dicts(self) -> typing.List[dict]:
        return self.goats.find({})

    def sync_goat(self, goat: Goat):
        sample_goat_dict = self.form_goat_dict()
        goat_dict = self.serialize_goat(goat)
        for line in sample_goat_dict:
            if line not in goat_dict:
                goat_dict.update({line: sample_goat_dict[line]})
        self.update_goat(goat.id, goat_dict)

    def sync_all_goats(self):
        for goat in self.all_goats:
            self.sync_goat(goat)

    def get_goat(self, goat_id):
        goat = self.goats.find_one({'id': goat_id})
        if not goat:
            return None
        return self.deserialize_goat(goat)

    def get_goat_dict(self, goat_id):
        goat = self.get_goat(goat_id)
        if not goat:
            return None
        return self.serialize_goat(goat)

    def deserialize_goat(self, goat) -> Goat:
        return self.factory.load(goat, Goat)

    def serialize_goat(self, goat: Goat) -> dict:
        return self.factory.dump(goat)

    def update_goat(self, goat_id, param, method='$set'):
        self.goats.update_one({'id': goat_id}, {method: param})

    def form_goat_dict(self, **kwargs):
        goat = {
            'id': self.max_goat_id + 1,
            'holder': 0,
            'name': 'Коза',
            'level': 0,
            'exp': 0,
            'type': 'common'
        }
        goat.update(kwargs)
        return goat

    def form_goat(self, **kwargs) -> Goat:
        goat_dict = self.form_goat_dict(**kwargs)
        return self.deserialize_goat(goat_dict)

    def create_goat(self, **kwargs) -> Goat:
        goat_dict = self.form_goat_dict(**kwargs)
        self.goats.insert_one(goat_dict)
        return self.deserialize_goat(goat_dict)

    def get_user_goats(self, user_id):
        return self.filter_goats({'holder': user_id})

    def filter_goats(self, query):
        goats = self.goats.find(query)
        return self.deserialize_goats(goats)

    def deserialize_goats(self, goats: list) -> typing.List[Goat]:
        return [self.deserialize_goat(goat) for goat in goats]

    def serialize_goats(self, goats: typing.List[Goat]) -> typing.List[dict]:
        return [self.serialize_goat(goat) for goat in goats]
