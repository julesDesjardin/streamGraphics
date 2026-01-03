import telebot
import queue
import time
import threading
from Common import LocalBot
from types import SimpleNamespace

SPLIT_SYMBOL = '\n£££'
COMMAND_SYMBOL = '$$$'
DATA_SPLIT_SYMBOL = '§§§'
SENDING_MESSAGES_DELAY = 3


class TelegramBot:

    def __init__(self, token, id, sender, receiver):
        if token == '':
            self.bot = LocalBot.LocalBot(receiver, self.messageHandlerLocal)
            self.id = 0
        else:
            self.bot = telebot.TeleBot(token)
            self.id = id
        if sender:
            self.sendQueue = queue.Queue()
            self.sendThread = threading.Thread(target=self.loopSendMessage)
            self.sendThread.daemon = True
            self.sendThread.start()
        if receiver:
            self.callbacks = dict([])
            if token != '':
                self.bot.register_channel_post_handler(self.messageHandler, commands=['streamCommand'])

    def messageHandlerLocal(self, messageText):
        if messageText.startswith('/streamCommand'):
            self.messageHandler(SimpleNamespace(text=messageText))

    def messageHandler(self, message):
        fullMessage = message.text.removeprefix('/streamCommand \n')
        for subCommand in fullMessage.split(SPLIT_SYMBOL):
            command, data = subCommand.split(COMMAND_SYMBOL)
            if command in self.callbacks:
                self.callbacks[command](data)

    def setMessageHandler(self, commands, function):
        for command in commands:
            self.callbacks[command] = function

    def startPolling(self):
        self.bot.polling()

    def sendMessage(self, command, data):
        self.sendQueue.put([command, data])

    def loopSendMessage(self):
        while True:
            messages = []
            while True:
                try:
                    messages.append(self.sendQueue.get(block=False))
                except queue.Empty:
                    break
            if len(messages) != 0:
                fullMessage = '/streamCommand \n' + SPLIT_SYMBOL.join([COMMAND_SYMBOL.join(message) for message in messages])
                self.bot.send_message(self.id, fullMessage)
            time.sleep(SENDING_MESSAGES_DELAY)

    def sendSimpleMessage(self, message):
        self.bot.send_message(self.id, message)
