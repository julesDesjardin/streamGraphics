import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json
import queue
import threading
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot


class CardsSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self, root, camerasCount):
        self.root = root
        self.camerasCount = camerasCount
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.queues = []
        for i in range(0, camerasCount):
            self.queues.append(queue.Queue())

    def botCallback(self, message):
        fullMessage = message.text.removeprefix('/cardData ')
        camera = int(fullMessage[0])
        data = fullMessage[2:]
        self.queues[camera].put(data)

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./', filetypes=(("JSON Files", "*.json"),
                                                    ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'botToken': self.botToken,
            'botChannelId': self.botChannelId
        }
        saveFile.write(json.dumps(saveSettingsJson, indent=4))

    def loadSettings(self):
        loadFile = tkinter.filedialog.askopenfile(initialdir='./', filetypes=(("JSON Files", "*.json"),
                                                  ("All Files", "*.*")), defaultextension='.json')
        try:
            loadSettingsJson = json.loads(loadFile.read())
        except:
            if loadFile is not None:
                tkinter.messagebox.showerror(title='File Error !', message='File is not a json file')
            return

        try:
            self.botToken = loadSettingsJson['botToken']
            self.botChannelId = loadSettingsJson['botChannelId']
        except:
            tkinter.messagebox.showerror(title='Settings Error !',
                                         message='Error in the Settings file, please make sure you selected the correct file and try to load again')
            return

        try:
            self.bot = TelegramBot.TelegramBot(self.botToken, self.botChannelId)
            self.bot.sendMessage('Bot Cards ready')
            self.bot.setMessageHandler(['cardData'], lambda message: self.botCallback(message))
            self.threadBot = threading.Thread(target=self.bot.startPolling)
            self.threadBot.daemon = True
            self.threadBot.start()
        except:
            tkinter.messagebox.showerror(
                title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct, and the application isn\'t already running')
            return

    def updateTelegramSettingsCloseButton(self, token, id, window):
        self.botToken = token
        self.botChannelId = id
        self.bot = TelegramBot.TelegramBot(token, id)
        self.bot.setMessageHandler(['cardData'], self.botCallback)
        self.threadBot = threading.Thread(target=self.bot.startPolling)
        self.threadBot.daemon = True
        self.threadBot.start()
        window.destroy()

    def updateTelegramSettings(self):
        telegramWindow = tk.Toplevel(self.root)
        telegramWindow.grab_set()
        telegramLabel = tk.Label(telegramWindow, text='Please enter Telegram settings')
        telegramLabel.pack(pady=20)
        tokenLabel = tk.Label(telegramWindow, text='TimeTower bot token')
        tokenLabel.pack(pady=5)
        tokenEntry = tk.Entry(telegramWindow, width=50)
        tokenEntry.insert(0, self.botToken)
        tokenEntry.pack(pady=5)
        idLabel = tk.Label(telegramWindow, text='Channel ID between bots')
        idLabel.pack(pady=5)
        idEntry = tk.Entry(telegramWindow, width=50)
        idEntry.insert(0, self.botChannelId)
        idEntry.pack(pady=5)
        telegramCloseButton = tk.Button(telegramWindow, text='Save Telegram Settings',
                                        command=lambda: self.updateTelegramSettingsCloseButton(tokenEntry.get(), idEntry.get(), telegramWindow))
        telegramCloseButton.pack(pady=20)

    def showFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black', highlightthickness=1)
        settingsLabel = tk.Label(frame, text='Settings', bg=self.BG_COLOR)
        settingsLabel.grid(column=0, row=0)
        telegramButton = tk.Button(frame, text='Change Telegram Settings', command=self.updateTelegramSettings)
        telegramButton.grid(column=0, row=1)
        saveButton = tk.Button(frame, text='Save Settings...', command=self.saveSettings)
        saveButton.grid(column=0, row=2)
        saveButton = tk.Button(frame, text='Load Settings...', command=self.loadSettings)
        saveButton.grid(column=0, row=3)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
