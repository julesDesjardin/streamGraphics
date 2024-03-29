import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json, urllib.request
import Stage
import constants

import sys
sys.path.append('.')
from Common import TelegramBot

class InterfaceSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self,root):
        self.root = root
        self.compId = ''
        self.wcif = {}
        self.rounds = {}
        self.groups = {}
        self.maxSeed = constants.MAX_SEED
        self.stages = []
        self.cardText = ''
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
    
    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'compId' : self.compId,
            'maxSeed' : self.maxSeed,
            'stages' : [(stage.backgroundColor, stage.textColor) for stage in self.stages],
            'cardText' : self.cardText,
            'botToken' : self.botToken,
            'botChannelId' : self.botChannelId
        }
        saveFile.write(json.dumps(saveSettingsJson, indent=4))
    
    def loadSettings(self):
        loadFile = tkinter.filedialog.askopenfile(initialdir='./',filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")), defaultextension='.json')
        loadSettingsJson = json.loads(loadFile.read())

        self.compId = loadSettingsJson['compId']
        self.reloadWCIF()
        self.maxSeed = loadSettingsJson['maxSeed']

        for stage in self.stages:
            stage.hideStage()
        self.stages = []
        for (stageBackgroundColor, stageTextColor) in loadSettingsJson['stages']:
            self.stages.append(Stage.Stage(self.root, self.wcif, stageBackgroundColor, stageTextColor))
        for stage in self.stages:
            stage.showStage()
        
        self.cardText = loadSettingsJson['cardText']
        self.botToken = loadSettingsJson['botToken']
        self.botChannelId = loadSettingsJson['botChannelId']
        self.bot = TelegramBot.TelegramBot(self.botToken,self.botChannelId)

    def updateCompIdCloseButton(self,compId,window):
        self.compId = compId
        try:
            self.reloadWCIF()
        except:
             tkinter.messagebox.showerror(title='Competition ID Error !', message='The WCIF was not found ! Please ensure that the competition ID is correct, you have access to the internet, and the WCA website is up')
        else:
            window.destroy()

    def updateCompId(self):
        compIdWindow = tk.Toplevel(self.root)
        compIdLabel = tk.Label(compIdWindow,text='Please enter competition ID to fetch the correct WCIF')
        compIdLabel.pack(padx=20,pady=5)
        compIdEntry = tk.Entry(compIdWindow,text=self.compId,width=50)
        compIdEntry.pack(padx=20,pady=5)
        compIdCloseButton = tk.Button(compIdWindow,text='Update and reload WCIF',command=lambda:self.updateCompIdCloseButton(compIdEntry.get(),compIdWindow))
        compIdCloseButton.pack(padx=20,pady=5)

    def reloadWCIF(self):
        jsonFile = urllib.request.urlopen(f'https://worldcubeassociation.org/api/v0/competitions/{self.compId}/wcif/public')
        self.wcif = json.loads(jsonFile.read())

    def updateMaxSeedCloseButton(self,maxSeed,window):
        try:
            self.maxSeed = int(maxSeed)
        except:
             tkinter.messagebox.showerror(title='Max Seed Error !', message='Error ! Please make sure the seed is a number')
        else:
            window.destroy()

    def updateMaxSeed(self):
        maxSeedWindow = tk.Toplevel(self.root)
        maxSeedLabel = tk.Label(maxSeedWindow,text='Please enter the maximum seed to be shown on stream')
        maxSeedLabel.pack(padx=20,pady=5)
        maxSeedEntry = tk.Entry(maxSeedWindow,text=self.maxSeed,width=20)
        maxSeedEntry.pack(padx=20,pady=5)
        maxSeedCloseButton = tk.Button(maxSeedWindow,text='Save max seed',command=lambda:self.updateMaxSeedCloseButton(maxSeedEntry.get(),maxSeedWindow))
        maxSeedCloseButton.pack(padx=20,pady=5)

    def updateStages(self):
        # TODO
        for stage in self.stages:
            stage.hideStage()
        stage = Stage.Stage(self.root, self.wcif, '#FFFFFF', '#000000')
        self.stages = [stage]
        stage.showStage()

    def updateCardTextCloseButton(self,cardText,window):
        self.cardText = cardText
        window.destroy()

    def updateCardText(self):
        cardTextWindow = tk.Toplevel(self.root)
        cardTextDescription = '''
Please enter the text to show on the card
This supports the following characters to be replaced by the appropriate value:
%name: Name of the competitor
%prSingle: PR single
%prAverage: PR average/mean
%nrSingle: National ranking single
%nrAverage: National ranking average/mean
%crSingle: Continental ranking single
%crAverage: Continental ranking average/mean
%wrSingle: World ranking single
%wrAverage: World ranking average/mean
%seed: Seed (based on PRs before the competition)
%previousRank: Place on the previous round (when applicable)
%previousSingle: Single on the previous round (when applicable)
%previousAverage: Average on the previous round (when applicable)
'''
        cardTextLabel = tk.Label(cardTextWindow,text=cardTextDescription,justify='left')
        cardTextLabel.pack(padx=20,pady=5)
        cardTextEntry = tk.Text(cardTextWindow)
        cardTextEntry.pack(padx=20,pady=5)
        cardTextCloseButton = tk.Button(cardTextWindow,text='Save card text',command=lambda:self.updateCardTextCloseButton(cardTextEntry.get('1.0','end-1c'),cardTextWindow))
        cardTextCloseButton.pack(padx=20,pady=5)

    def updateTelegramSettingsCloseButton(self,token,id,window):
        self.botToken = token
        self.botChannelId = id
        self.bot = TelegramBot.TelegramBot(token,id)
        window.destroy()

    def updateTelegramSettings(self):
        telegramWindow = tk.Toplevel(self.root)
        telegramLabel = tk.Label(telegramWindow,text='Please enter Telegram settings')
        telegramLabel.pack(pady=20)
        tokenLabel = tk.Label(telegramWindow,text='Interface bot token')
        tokenLabel.pack(pady=5)
        tokenEntry = tk.Entry(telegramWindow,width=50)
        tokenEntry.pack(pady=5)
        idLabel = tk.Label(telegramWindow,text='Channel ID between interface and card bots')
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
        reloadButton = tk.Button(frame,text='Reload WCIF',command=self.reloadWCIF)
        reloadButton.grid(column=0,row=2)
        maxSeedButton = tk.Button(frame,text='Change Max Seed',command=self.updateMaxSeed)
        maxSeedButton.grid(column=0,row=3)
        stagesButton = tk.Button(frame,text='Setup stages',command=self.updateStages)
        stagesButton.grid(column=0,row=4)
        cardTextButton = tk.Button(frame,text='Change text on card',command=self.updateCardText)
        cardTextButton.grid(column=0, row=5)
        telegramButton = tk.Button(frame,text='Change Telegram Settings',command=self.updateTelegramSettings)
        telegramButton.grid(column=0,row=6)
        saveButton = tk.Button(frame,text='Save Settings...',command=self.saveSettings)
        saveButton.grid(column=0,row=7)
        saveButton = tk.Button(frame,text='Load Settings...',command=self.loadSettings)
        saveButton.grid(column=0,row=8)
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
        frame.rowconfigure(4, pad=20)
        frame.rowconfigure(5, pad=20)
        frame.rowconfigure(6, pad=20)
        frame.rowconfigure(7, pad=20)
        frame.rowconfigure(8, pad=20)

