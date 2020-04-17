from telebot import TeleBot
import time

class BotUtil(TeleBot):

    def __init__(self, token, creator=None):
        super().__init__(token)
        self.bot = TeleBot(token)
        self.__group_admins = ['administrator', 'creator']
        self.__creator = creator

    def edit_message(self, message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
        return self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                          reply_markup=reply_markup, parse_mode=parse_mode)

    def reply(self, chat_id, message_text, message_id, reply_markup=None, parse_mode=None):
        return self.bot.send_message(chat_id, message_text, reply_to_message_id=message_id, reply_markup=reply_markup,
                                     parse_mode=parse_mode)

    def get_link(self, name, user_id):
        return '<a href="tg://user?id={}">{}</a>'.format(user_id, name)

    def is_admin(self, chat, user):
        chat_member = self.bot.get_chat_member(chat, user)
        if chat_member.status in self.__group_admins:
            return True
        else:
            return False

    def __admin_checks(self, chat, user, admin_user):
        if chat.type == "private":
            self.bot.send_message(chat.id, "Административные команды не работают в личных сообщениях.")
            return False
        if self.is_admin(chat.id, user.id):
            self.bot.send_message(chat.id, "Вы пытаетесь ограничить администратора.")
            return False
        if not self.is_admin(chat.id, admin_user.id):
            self.bot.send_message(chat.id, "Вы не администратор.")
            return False
        if not self.is_admin(chat.id, self.bot.get_me().id):
            self.bot.send_message(chat.id, "Я не администратор.")
            return False
        return True

    def mute(self, chat, user, admin_user, for_date=0, reason=""):
        if not self.__admin_checks(chat, user, admin_user):
            return
        now_time = int(time.time())
        until_date = now_time + for_date
        time_text = "секунд"
        date_text = for_date
        if for_date > 60:
            date_text = "минут"
            time_text = str(for_date / 60)
        elif for_date > 3600:
            date_text = "часов"
            time_text = str(for_date / 3600)
        elif for_date > 86400:
            date_text = "дней"
            time_text = str(for_date / 86400)
        tts = 'Пользователь {} ограничен на {} {}.'.format(self.get_link(user.first_name, user.id), time_text, date_text)
        if for_date < 60:
            tts = "Пользователь {} ограничен навсегда.".format(self.get_link(user.first_name, user.id))
        tts += "\nПричина: {}".format(reason)
        self.bot.restrict_chat_member(chat.id, user.id, until_date=until_date)
        self.bot.send_message(chat.id, tts, parse_mode="HTML")

    def ban(self, chat, user, admin_user, for_date=0, reason=""):
        if not self.__admin_checks(chat, user, admin_user):
            return
        now_time = int(time.time())
        until_date = now_time + for_date
        time_text = "секунд"
        date_text = for_date
        if 60 < for_date < 3600:
            date_text = "минут"
            time_text = str(for_date / 60)
        elif 3600 < for_date < 86400:
            date_text = "часов"
            time_text = str(for_date / 3600)
        elif for_date > 86400:
            date_text = "дней"
            time_text = str(for_date / 86400)
        tts = 'Пользователь {} заблокирован на {} {}.'.format(self.get_link(user.first_name, user.id), time_text, date_text)
        if for_date < 60:
            tts = "Пользователь {} заблокирован навсегда.".format(self.get_link(user.first_name, user.id))
        tts += "\nПричина: {}".format(reason)
        self.bot.kick_chat_member(chat.id, user.id, until_date=until_date)
        self.bot.send_message(chat.id, tts, parse_mode="HTML")

    def report(self, text):
        if self.__creator:
            print(text)
            return self.bot.send_message(self.__creator, text)
