# All rights for this file belong to Fyodor Doletov <doletov.fyodor@yandex.ru>. Do NOT edit these comments
# You can copy this file, modify it (but don't edit these comments) and use in your own project for free

"""
USAGE EXAMPLE
from manybotslib import BotsRunner
runner = BotsRunner([admin1, admin2, admin3]) # pass empty list if you don't want to receive error messages on fail
runner.add_bot("Coolbot", bot1)
runner.add_bot("Coolbot", bot2)
runner.add_bot("Controller", controller)
runner.set_main_bot(controller)
runner.run()
"""

from threading import Thread
import traceback


class BotsRunner:

    def __init__(self, admins = list()):
        self.__bots = dict()
        self.__bots_status = dict()
        self.__main_bot = None
        self.__admins = list(admins)

    def get_status(self):
        text = "Статус работы ботов:\n\n"
        for botname in self.__bots_status:
            if self.__bots_status[botname]:
                text += "✅ " + botname + " - Online!\n"
            else:
                text += "❌ " + botname + " - Offline!\n"
        return text

    def add_bot(self, name, bot):
        self.__bots.update({name: bot})
        self.__bots_status.update({name: False})

    def set_main_bot(self, bot):
        self.__main_bot = bot

    def run(self):
        for botname in self.__bots:
            Thread(target=self.__poll, args=[botname], name=botname).start()

    def __warn_about_fail(self, botname):
        text = "Бот " + botname + " отвалился!\n\n"
        text += self.get_status() + "\n\n"
        text += "<code>" + traceback.format_exc() + "</code>"
        for adm in self.__admins:
            self.__main_bot.send_message(adm, text, parse_mode="HTML")

    def __poll(self, botname):
        try:
            self.__bots_status.update({botname: True})
            self.__bots[botname].polling(none_stop=True, timeout=600)
        except Exception:
            self.__bots_status.update({botname: False})
            self.__warn_about_fail(botname)
            
