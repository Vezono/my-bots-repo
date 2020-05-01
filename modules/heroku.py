import heroku3

import config


class Heroku():
    def __init__(self, bot):
        self.bot = bot
        self.app = heroku3.from_key(config.environ['heroku_key']).apps()['gbball-great-host']
        self.last_log = ''
