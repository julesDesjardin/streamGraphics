import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json, queue, threading
import utils

import sys
sys.path.append('.')
from Common import TelegramBot

class TimeTowerSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self,root):
        self.root = root
        self.compId = 0
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.queue = queue.Queue()

    def botCallback(self,message,compId):

        fullMessage = message.text.removeprefix('/timeTowerEvent ')
        fullMessageSplit = fullMessage.split()
        event = fullMessageSplit[0]
        number = int(fullMessageSplit[1])

        query = f'''
        query MyQuery {{
            competition(id: "{compId}") {{
                competitionEvents {{
                    event {{
                        id
                    }}
                    rounds {{
                        id
                        number
                    }}
                }}
            }}
        }}
        '''

        result = utils.getQueryResult(query)
        for competitionEvent in result['competition']['competitionEvents']:
            if(competitionEvent['event']['id'] == event):
                for round in competitionEvent['rounds']:
                    if(round['number'] == number):
                        self.queue.put((int(round['id']), utils.CRITERIA[event]))
                        return

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'compId' : self.compId,
            'botToken' : self.botToken,
            'botChannelId' : self.botChannelId
        }
        saveFile.write(json.dumps(saveSettingsJson, indent=4))
    
    def loadSettings(self):
        loadFile = tkinter.filedialog.askopenfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        loadSettingsJson = json.loads(loadFile.read())

        self.compId = loadSettingsJson['compId']
        self.botToken = loadSettingsJson['botToken']
        self.botChannelId = loadSettingsJson['botChannelId']
        self.bot = TelegramBot.TelegramBot(self.botToken,self.botChannelId)
        self.bot.setMessageHandler(['timeTowerEvent'], lambda message:self.botCallback(message, self.compId))
        self.threadBot = threading.Thread(target=self.bot.startPolling)
        self.threadBot.daemon = True
        self.threadBot.start()
    
    def updateCompIdCloseButton(self,compId,window):
        try:
            self.compId = int(compId)
        except:
             tkinter.messagebox.showerror(title='Competition ID Error !', message='The ID must be a number! This is the WCA Live ID, not the WCA competition ID.')
        else:
            window.destroy()

    def updateCompId(self):
        compIdWindow = tk.Toplevel(self.root)
        compIdLabel = tk.Label(compIdWindow,text='Please enter competition ID to fetch the correct WCIF\nThis is NOT the WCA ID but the Live ID (4 digits)')
        compIdLabel.pack(padx=20,pady=5)
        compIdEntry = tk.Entry(compIdWindow,text=self.compId,width=50)
        compIdEntry.pack(padx=20,pady=5)
        compIdCloseButton = tk.Button(compIdWindow,text='Update ID',command=lambda:self.updateCompIdCloseButton(compIdEntry.get(),compIdWindow))
        compIdCloseButton.pack(padx=20,pady=5)

    def updateTelegramSettingsCloseButton(self,token,id,window):
        self.botToken = token
        self.botChannelId = id
        self.bot = TelegramBot.TelegramBot(token,id)
        self.bot.setMessageHandler(['timeTowerEvent'], lambda message:self.botCallback(message, self.compId))
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
        compIdButton = tk.Button(frame,text='Update competition ID',command=self.updateCompId)
        compIdButton.grid(column=0,row=1)
        telegramButton = tk.Button(frame,text='Change Telegram Settings',command=self.updateTelegramSettings)
        telegramButton.grid(column=0,row=2)
        saveButton = tk.Button(frame,text='Save Settings...',command=self.saveSettings)
        saveButton.grid(column=0,row=3)
        saveButton = tk.Button(frame,text='Load Settings...',command=self.loadSettings)
        saveButton.grid(column=0,row=4)
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
        frame.rowconfigure(4, pad=20)