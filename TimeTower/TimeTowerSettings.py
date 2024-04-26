import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json, queue, threading
import utils

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot
import TimeTowerContent, constants

class TimeTowerSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self,root):
        self.root = root
        self.compId = 0
        self.delay = 0
        self.region = 'World'
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.queue = queue.Queue()
        self.content = None
        self.stepXmax = constants.DEFAULT_STEPS_X

    def timeTowerEventCallback(self,message):

        fullMessage = message.text.removeprefix('/timeTowerEvent ')
        fullMessageSplit = fullMessage.split()
        event = fullMessageSplit[0]
        number = int(fullMessageSplit[1])

        query = f'''
        query MyQuery {{
            competition(id: "{self.compId}") {{
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

    def timeTowerExpandCallback(self,message):
        fullMessage = message.text.removeprefix('/timeTowerExpand ')
        fullMessageSplit = fullMessage.split()
        competitor = int(fullMessageSplit[0])
        enable = fullMessageSplit[1]
        for line in self.content.lines:
            if competitor == line.competitorRegistrantId:
                if enable == '1':
                    line.expandRequest = True
                else:
                    line.reduceRequest = True

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'compId' : self.compId,
            'delay' : self.delay,
            'region' : self.region,
            'botToken' : self.botToken,
            'botChannelId' : self.botChannelId
        }
        saveFile.write(json.dumps(saveSettingsJson, indent=4))
    
    def loadSettings(self):
        loadFile = tkinter.filedialog.askopenfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        try:
            loadSettingsJson = json.loads(loadFile.read())
        except:
            if loadFile is not None:
                tkinter.messagebox.showerror(title='File Error !', message='File is not a json file')
            return

        try:
            self.compId = loadSettingsJson['compId']
            self.delay = loadSettingsJson['delay']
            self.region = loadSettingsJson['region']
            self.botToken = loadSettingsJson['botToken']
            self.botChannelId = loadSettingsJson['botChannelId']
        except:
            tkinter.messagebox.showerror(title='Settings Error !', message='Error in the Settings file, please make sure you selected the correct file and try to load again')
            return
        try:
            self.bot = TelegramBot.TelegramBot(self.botToken,self.botChannelId)
            self.bot.sendMessage('Bot TimeTower ready')
            self.bot.setMessageHandler(['timeTowerEvent'], lambda message:self.timeTowerEventCallback(message))
            self.bot.setMessageHandler(['timeTowerExpand'], lambda message:self.timeTowerExpandCallback(message))
            self.threadBot = threading.Thread(target=self.bot.startPolling)
            self.threadBot.daemon = True
            self.threadBot.start()
        except:
            tkinter.messagebox.showerror(title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct, and the application isn\'t already running')
            return

        roundId = 0
        criteria = ''
        if self.content is not None:
            self.content.stop = 1
            roundId = self.content.roundId
            criteria = self.content.criteria
        self.content = TimeTowerContent.TimeTowerContent(self.root, self.queue, self.region, *constants.DEFAULT_TIMETOWER_PARAMETERS, self.delay, roundId, criteria, self.stepXmax)
        self.content.showFrame()
        self.content.mainLoop()
    
    def updateCompIdCloseButton(self,compId,window):
        try:
            self.compId = int(compId)
        except:
            tkinter.messagebox.showerror(title='Competition ID Error !', message='The ID must be a number! This is the WCA Live ID, not the WCA competition ID.')
        else:
            window.destroy()

    def updateCompId(self):
        compIdWindow = tk.Toplevel(self.root)
        compIdWindow.grab_set()
        compIdLabel = tk.Label(compIdWindow,text='Please enter competition ID to fetch the correct WCIF\nThis is NOT the WCA ID but the Live ID (4 digits)')
        compIdLabel.pack(padx=20,pady=5)
        compIdEntry = tk.Entry(compIdWindow,width=50)
        compIdEntry.insert(0, self.compId)
        compIdEntry.pack(padx=20,pady=5)
        compIdCloseButton = tk.Button(compIdWindow,text='Update ID',command=lambda:self.updateCompIdCloseButton(compIdEntry.get(),compIdWindow))
        compIdCloseButton.pack(padx=20,pady=5)

    def updateDelayCloseButton(self,delay,window):
        try:
            self.delay = int(delay)
        except:
            tkinter.messagebox.showerror(title='Delay Error !', message='The delay must be a whole number ! (No units needed)')
        else:
            roundId = 0
            criteria = ''
            if self.content is not None:
                self.content.stop = 1
                self.content.threadResults.join()
                roundId = self.content.roundId
                criteria = self.content.criteria
            self.content = TimeTowerContent.TimeTowerContent(self.root, self.queue, self.region, *constants.DEFAULT_TIMETOWER_PARAMETERS, self.delay, roundId, criteria, self.stepXmax)
            self.content.showFrame()
            self.content.mainLoop()
            window.destroy()

    def updateDelay(self):
        delayWindow = tk.Toplevel(self.root)
        delayWindow.grab_set()
        delayLabel = tk.Label(delayWindow,text='Please enter the delay (in ms) between 2 consecutive fetches to Live.\nPlease take into account that this does NOT include the time needed to retrieve data from Live and display it.')
        delayLabel.pack(padx=20,pady=5)
        delayEntry = tk.Entry(delayWindow,width=50)
        delayEntry.insert(0, self.delay)
        delayEntry.pack(padx=20,pady=5)
        delayCloseButton = tk.Button(delayWindow,text='Update delay',command=lambda:self.updateDelayCloseButton(delayEntry.get(),delayWindow))
        delayCloseButton.pack(padx=20,pady=5)

    def checkRegionSeparator(self,regionBox):
        if regionBox.get() == constants.SEPARATOR:
            regionBox.set('World')

    def updateRegionCloseButton(self,region,window):
        self.region = region
        window.destroy()

    def updateRegion(self):
        regionWindow = tk.Toplevel(self.root)
        regionWindow.grab_set()
        regionLabel = tk.Label(regionWindow,text='Please choose a region (country or continent) if you want local competitors to be highlighted, so you can see the local results more easily.\nThe "World" option highlights everyone the same.')
        regionLabel.pack(padx=20,pady=5)
        regionBox = ttk.Combobox(regionWindow)
        regionBox['values'] = constants.REGION_OPTIONS
        regionBox.set(self.region)
        regionBox['state'] = 'readonly'
        regionBox.bind('<<ComboboxSelected>>', lambda event:self.checkRegionSeparator(regionBox))
        regionBox.pack(padx=20,pady=5)
        regionCloseButton = tk.Button(regionWindow,text='Update region', command=lambda:self.updateRegionCloseButton(regionBox.get(), regionWindow)) 
        regionCloseButton.pack(padx=20,pady=5)

    def updateTelegramSettingsCloseButton(self,token,id,window):
        self.botToken = token
        self.botChannelId = id
        self.bot = TelegramBot.TelegramBot(token,id)
        self.bot.setMessageHandler(['timeTowerEvent'], lambda message:self.timeTowerEventCallback(message))
        self.bot.setMessageHandler(['timeTowerExpand'], lambda message:self.timeTowerExpandCallback(message))
        self.threadBot = threading.Thread(target=self.bot.startPolling)
        self.threadBot.daemon = True
        self.threadBot.start()

        window.destroy()

    def updateTelegramSettings(self):
        telegramWindow = tk.Toplevel(self.root)
        telegramWindow.grab_set()
        telegramLabel = tk.Label(telegramWindow,text='Please enter Telegram settings')
        telegramLabel.pack(pady=20)
        tokenLabel = tk.Label(telegramWindow,text='TimeTower bot token')
        tokenLabel.pack(pady=5)
        tokenEntry = tk.Entry(telegramWindow,width=50)
        tokenEntry.insert(0, self.botToken)
        tokenEntry.pack(pady=5)
        idLabel = tk.Label(telegramWindow,text='Channel ID between bots')
        idLabel.pack(pady=5)
        idEntry = tk.Entry(telegramWindow,width=50)
        idEntry.insert(0, self.botChannelId)
        idEntry.pack(pady=5)
        telegramCloseButton = tk.Button(telegramWindow,text='Save Telegram Settings',command=lambda:self.updateTelegramSettingsCloseButton(tokenEntry.get(),idEntry.get(),telegramWindow))
        telegramCloseButton.pack(pady=20)

    def showFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black',highlightthickness=1)
        settingsLabel = tk.Label(frame,text='Settings',bg=self.BG_COLOR)
        settingsLabel.grid(column=0,row=0)
        compIdButton = tk.Button(frame,text='Update competition ID',command=self.updateCompId)
        compIdButton.grid(column=0,row=1)
        delayButton = tk.Button(frame,text='Update refresh delay',command=self.updateDelay)
        delayButton.grid(column=0,row=2)
        regionButton = tk.Button(frame,text='Update championship region',command=self.updateRegion)
        regionButton.grid(column=0,row=3)
        telegramButton = tk.Button(frame,text='Change Telegram Settings',command=self.updateTelegramSettings)
        telegramButton.grid(column=0,row=4)
        saveButton = tk.Button(frame,text='Save Settings...',command=self.saveSettings)
        saveButton.grid(column=0,row=5)
        saveButton = tk.Button(frame,text='Load Settings...',command=self.loadSettings)
        saveButton.grid(column=0,row=6)
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
        frame.rowconfigure(4, pad=20)
        frame.rowconfigure(5, pad=20)
        frame.rowconfigure(6, pad=20)