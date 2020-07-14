from telebot.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup


class Views:
    def __init__(self):
        self.ru = {}

    def rusify(self, text):
        rus = self.ru.get(text)
        if not rus:
            return text
        return rus

    def form_register_keyboard(self, user_doc):
        kb = Markup()
        for line in user_doc:
            if line in ['id', '_id', 'money', 'inv']:
                continue
            if isinstance(user_doc[line], dict):
                if
                    kb.add(Button(text=f'{self.rusify(line)} - {self.rusify(user_doc["body"]["height"])}',
                                  callback_data=line))
            kb.add(Button(text=f'{self.rusify(line)} - {user_doc[line]}', callback_data=line))
