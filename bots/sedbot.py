from modules.coach import Coach

coach = Coach()

import re
from subprocess import Popen, PIPE

import config
from modules.funcs import BotUtil

bot = BotUtil(config.environ['sedbot'], config.creator)


def sed(pattern, text):
    regular = pattern.split("/", 2)[1]
    replacement = pattern.split("/", 2)[2]
    if regular and replacement:
        output = f"{text.replace(regular, replacement)}"
        return output


def newsed(pattern, text):
    cmd = ['/bin/sed', '-e', pattern, '-e', 'tx', '-e', 'd', '-e', ':x']
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False)
    p.stdin.write(text.encode())
    out, err = p.communicate()
    out = out.decode()
    err = err.decode()
    if err:
        return err
    if out:
        return out
    return "Пусто."


def py_sed(pattern, text):
    regular = pattern.split("/", 3)[1]
    replacement = pattern.split("/", 3)[2]
    return re.sub(regular, replacement, text)


@bot.message_handler()
def handler(m):
    text = m.text
    if not m.reply_to_message:
        return
    if not text.startswith("s/"):
        return
    if text.count('/') == 2:
        text += '/'
    elif text.count('/') != 3:
        return
    try:
        text = py_sed(m.text, m.reply_to_message.text)
    except:
        bot.reply_to(m, 'Ошибка. Обратитесь к @gbball за помощью.')
        return
    bot.reply_to(m.reply_to_message, text)


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
