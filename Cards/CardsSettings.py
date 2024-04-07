import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json, queue, threading
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot

class CardsSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self,root):
        self.root = root
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.queueLeft = queue.Queue()
        self.queueRight = queue.Queue()

    def botCallback(self, message):
        fullMessage = message.text.removeprefix('/cardData ')
        camera = fullMessage[0]
        data = fullMessage[2:]
        if camera == '0':
            self.queueLeft.put(data)
        elif camera == '1':
            self.queueRight.put(data)

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'botToken' : self.botToken,
            'botChannelId' : self.botChannelId
        }
        saveFile.write(json.dumps(saveSettingsJson, indent=4))
    
    def loadSettings(self):
        loadFile = tkinter.filedialog.askopenfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        loadSettingsJson = json.loads(loadFile.read())

        self.botToken = loadSettingsJson['botToken']
        self.botChannelId = loadSettingsJson['botChannelId']
        self.bot = TelegramBot.TelegramBot(self.botToken,self.botChannelId)
        self.bot.setMessageHandler(['cardData'], lambda message:self.botCallback(message, self.compId))
        self.threadBot = threading.Thread(target=self.bot.startPolling)
        self.threadBot.daemon = True
        self.threadBot.start()

    def updateTelegramSettingsCloseButton(self,token,id,window):
        self.botToken = token
        self.botChannelId = id
        self.bot = TelegramBot.TelegramBot(token,id)
        self.bot.setMessageHandler(['cardData'], self.botCallback)
        self.threadBot = threading.Thread(target=self.bot.startPolling)
        self.threadBot.daemon = True
        self.threadBot.start()
        window.destroy()

    def updateTelegramSettings(self):
        telegramWindow = tk.Toplevel(self.root)
        telegramLabel = tk.Label(telegramWindow,text='Please enter Telegram settings')
        telegramLabel.pack(pady=20)
        tokenLabel = tk.Label(telegramWindow,text='TimeTower bot token')
        tokenLabel.pack(pady=5)
        tokenEntry = tk.Entry(telegramWindow,width=50)
        tokenEntry.pack(pady=5)
        idLabel = tk.Label(telegramWindow,text='Channel ID between bots')
        idLabel.pack(pady=5)
        idEntry = tk.Entry(telegramWindow,width=50)
        idEntry.pack(pady=5)
        telegramCloseButton = tk.Button(telegramWindow,text='Save Telegram Settings',command=lambda:self.updateTelegramSettingsCloseButton(tokenEntry.get(),idEntry.get(),telegramWindow))
        telegramCloseButton.pack(pady=20)

    def showFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black',highlightthickness=1)
        settingsLabel = tk.Label(frame,text='Settings',bg=self.BG_COLOR)
        settingsLabel.grid(column=0,row=0)
        telegramButton = tk.Button(frame,text='Change Telegram Settings',command=self.updateTelegramSettings)
        telegramButton.grid(column=0,row=1)
        saveButton = tk.Button(frame,text='Save Settings...',command=self.saveSettings)
        saveButton.grid(column=0,row=2)
        saveButton = tk.Button(frame,text='Load Settings...',command=self.loadSettings)
        saveButton.grid(column=0,row=3)
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)