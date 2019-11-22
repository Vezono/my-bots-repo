import random
import telebot
import pymongo
from pymongo import MongoClient
import traceback
bot = telebot.TeleBot(os.environ['chatbot'])
client = pymongo.MongoClient(os.environ['database2'])
db = client.test
col = db.chatting
#print(col.find_one({'group_id':{'$exists':True}})['msgs_to_index'])

def write_to_db(m):
	if m.reply_to_message and m.text != None and m.reply_to_message.text != None and m.reply_to_message.from_user.is_bot != True and not m.reply_to_message.text.startswith('@') and not m.reply_to_message.text.startswith('/'):
		col.update_one({'group_id':m.chat.id},
				{'$push':{'msgs_to_index': m.reply_to_message.text.lower()}},
				upsert=True)
		col.update_one({'group_id':m.chat.id},
				{'$push':{m.reply_to_message.text.lower().replace('.', 'dot_replace'): m.text}},
				upsert=True)

@bot.message_handler(content_types='text')
def chatting(m):
	try:
		if col.find_one({'group_id':m.chat.id}):
			msgs_to_index = col.find_one({'group_id':m.chat.id})['msgs_to_index']
			if random.randint(1, 3) % 3 == 0:
				if m.text.lower() in msgs_to_index and m.reply_to_message == None or m.text in msgs_to_index and m.reply_to_message.from_user.is_bot != True:
					answer = col.find_one({'group_id':m.chat.id})[m.text.lower().replace('.', 'dot_replace')]
					answer = random.choice(answer)
					bot.send_message(m.chat.id, answer, reply_to_message_id = m.message_id)				
				else:
					return write_to_db(m)
		else:
			return write_to_db(m)

	except:
		bot.send_message(admin, traceback.format_exc())


bot.polling()
