import telebot

class TelegramBot:
    
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.id = message.chat.id
            print('/start has been sent!')
            self.bot.stop_polling()

    def setMessageHandler(self, commands, function):
        handlerDict = dict(
            function=function,
            filters=dict(
                commands=commands,
            )
        )
        self.channel.add_message_handler(handlerDict)

    def startPolling(self):
        self.bot.polling()
    
    def sendMessage(self, message):
        self.bot.send_message(self.id, message)