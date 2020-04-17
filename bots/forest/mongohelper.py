import config


class MongoHelper:

    def __init__(self, client):
        self.__client = client
        self.__games = client.forest.games

    def create_chat(self, chat_id):
        commit = {
            'id': chat_id,
            'admin': None,
            'players': {},
            'air': 100,
            'trees': 6000,
            'year': 0,
            'active': False,
            'game_started': False
        }
        self.__games.insert_one(commit)

    def create_game(self, chat_id, game_admin):
        commit = {
            'id': chat_id,
            'admin': game_admin,
            'players': {},
            'year': 0,
            'active': True,
            'game_started': False
        }
        self.__games.update_one({'id': chat_id}, {'$set': commit})

    def delete_game(self, chat_id):
        commit = {'admin': None,
                  'players': {},
                  'active': False,
                  'game_started': False
                  }
        self.__games.update_one({'id': chat_id}, {'$set': commit})

    def start_game(self, chat_id):
        self.__games.update_one({'id': chat_id}, {'$set': {'game_started': True}})

    def find_game(self, chat_id):
        return self.__games.find_one({'id': chat_id})

    def join_game(self, chat_id, user):
        game = self.find_game(chat_id)
        players = game['players']
        player = {
            'id': user.id,
            'name': user.first_name,
            'country': None,
            'res': {
                'food': 1,
                'water': 1,
                'materials': 1,
                'od': 3
            },
            'growth': {
                'food': 0,
                'water': 0,
                'materials': 0
            }
            # 'farms': [],
        }
        players.update({str(user.id): player})
        self.__games.update_one({'id': chat_id}, {'$set': {'players': players}})

    def leave_game(self, chat_id, user):
        game = self.find_game(chat_id)
        players = game['players']
        del players[str(user.id)]
        self.__games.update_one({'id': chat_id}, {'$set': {'players': players}})

    def set_country(self, chat_id, user, country):
        game = self.find_game(chat_id)
        players = game['players']
        player = players[str(user.id)]
        player['country'] = country
        players.update({str(user.id): player})
        self.__games.update_one({'id': chat_id}, {'$set': {'players': players}})

    def give_res(self, chat_id, user, resource, count):
        game = self.find_game(chat_id)
        players = game['players']
        try:
            if not players[str(user['id'])]['res'].get(resource):
                players[str(user['id'])]['res'][resource] = 0
            players[str(user['id'])]['res'][resource] += count
        except TypeError:
            if not players[str(user.id)]['res'].get(resource):
                players[str(user.id)]['res'][resource] = 0
            players[str(user.id)]['res'][resource] += count
        self.__games.update_one({'id': chat_id}, {'$set': {'players': players}})

    def give_growth(self, chat_id, user, resource, count, reason):
        game = self.find_game(chat_id)
        players = game['players']
        try:
            if not players[str(user['id'])]['res'].get(resource):
                players[str(user['id'])]['res'][resource] = 0
            if not players[str(user['id'])]['growth'].get(resource):
                players[str(user['id'])]['growth'][resource] = 0
            players[str(user['id'])]['growth'][resource] += count
            # farm_commit = {'res': resource, 'count': count, 'reason': reason}
            # players[str(user['id'])]['farms'].append(farm_commit)
        except TypeError:
            if not players[str(user.id)]['res'].get(resource):
                players[str(user.id)]['res'][resource] = 0
            if not players[str(user.id)]['growth'].get(resource):
                players[str(user.id)]['growth'][resource] = 0
            players[str(user.id)]['growth'][resource] += count
            # farm_commit = {'res': resource, 'count': count, 'reason': reason}
            # players[str(user['id'])]['farms'].append(farm_commit)
        self.__games.update_one({'id': chat_id}, {'$set': {'players': players}})

    def next_turn(self, chat_id):
        game = self.find_game(chat_id)
        players = game['players']
        for player in players:
            for growing_res in players[player]['growth']:
                players[player]['res'][growing_res] += players[player]['growth'][growing_res]
            players[player]['res']['od'] = 3
        self.__games.update_one({'id': chat_id}, {'$set': {'players': players}})
        self.__games.update_one({'id': chat_id}, {'$inc': {'year': 1}})

    def set_air(self, chat_id, count):
        game = self.find_game(chat_id)
        self.__games.update_one({'id': chat_id}, {'$inc': {'air': count}})

    def set_trees(self, chat_id, count):
        game = self.find_game(chat_id)
        self.__games.update_one({'id': chat_id}, {'$inc': {'trees': count}})