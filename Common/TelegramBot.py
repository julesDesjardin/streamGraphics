import telebot


class TelegramBot:

    def __init__(self, token, id):
        self.bot = telebot.TeleBot(token)
        self.id = id

    def setMessageHandler(self, commands, function):
        self.bot.register_channel_post_handler(function, commands=commands)

    def startPolling(self):
        self.bot.polling()

    def sendMessage(self, message):
        self.bot.send_message(self.id, message)
