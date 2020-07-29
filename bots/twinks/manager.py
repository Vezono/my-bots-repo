from pyrogram import Client


class Manager:
    def __init__(self, count, api_id, api_hash):
        self.clients = {}
        for i in range(count):
            client = Client(f"{i}", api_id=api_id, api_hash=api_hash)
            client.start()
            profile = client.get_me()
            self.clients.update({
                profile.id: client
            })
            print(f'{i}: {profile.id} - {profile.first_name}')
            client.stop()

    def earn_yuliacoins(self, chat, to_whom):
        success = 0
        for client in self.clients:
            try:
                client = self.clients[client]
                client.start()
                client.send_message(chat, '/getcoins')
                client.send_message(chat, '/give 300', reply_to_message_id=to_whom)
                client.stop()
                success += 1
            except:
                continue
        return f'success {success}/{len(self.clients)}'
