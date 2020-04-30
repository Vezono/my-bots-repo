import heroku3

import config


class Heroku:
    def __init__(self):
        self.app = heroku3.from_key(config.environ['heroku_key']).apps()['gbball-great-host']
