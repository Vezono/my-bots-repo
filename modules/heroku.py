import time

import heroku3

import config


class Heroku():
    def __init__(self, bot):
        self.bot = bot
        self.app = heroku3.from_key(config.environ['heroku_key']).apps()['gbball-great-host']
        self.last_log = ''
        self.polling()

    def polling(self):
        time.sleep(1)
        if self.app.get_log(lines=1) == self.last_log:
            self.polling()
        self.last_log = self.app.get_log(lines=1)
        self.bot.report(self.last_log, quiet=True)
