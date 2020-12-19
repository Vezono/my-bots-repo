from modules.coach import Coach

coach = Coach()

import telebot
import config
import nmap

token = config.environ['mystat_bot']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['nmap'])
def text_handler(m):
    bot.reply_to(m, 'Запускаю...')
    nm = nmap.PortScanner()
    bot.reply_to(m, 'Сканер создан...')
    nm.scan(m.text.split()[1], arguments='-vvv -Pn -sV')
    bot.reply_to(m, 'Скан окончен! Вывожу результат!')
    tts = ''
    for host in nm.all_hosts():
        tts += 'Host : %s (%s)\n' % (host, nm[host].hostname())
        tts += 'State : %s\n\n' % nm[host].state()
        for proto in nm[host].all_protocols():
            tts += 'Protocol : %s\n' % proto
            lport = nm[host][proto].keys()
            sorted(list(lport))
            for port in lport:
                tts += 'port : %s\tstate : %s\n' % (port, nm[host][proto][port]['state'])
    bot.reply_to(m, tts)


from modules.bot_keeper import keeper

keeper.bots_to_run.update({bot.get_me().first_name: bot})
print(f'{bot.get_me().first_name} booted in {coach.time()}.')
