import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json
import urllib.request
import Stage
import WCIFParse
import constants

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot


class InterfaceSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self, root):
        self.root = root
        self.compId = ''
        self.wcif = {}
        self.rounds = {}
        self.groups = {}
        self.maxSeed = constants.MAX_SEED
        self.stages = []
        self.exampleStages = []
        self.cardText = ''
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./', filetypes=(("JSON Files", "*.json"),
                                                    ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'compId': self.compId,
            'maxSeed': self.maxSeed,
            'stages': [(stage.backgroundColor, stage.textColor, stage.venue, stage.room) for stage in self.stages],
            'cardText': self.cardText,
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
            self.compId = loadSettingsJson['compId']
            try:
                self.reloadWCIF()
            except:
                tkinter.messagebox.showerror(
                    title='Competition ID Error !', message='The WCIF was not found ! Please ensure that the competition ID is correct, you have access to the internet, and the WCA website is up')
                return
            self.maxSeed = loadSettingsJson['maxSeed']

            for stage in self.stages:
                stage.hideStage()
            self.stages = []
            for (stageBackgroundColor, stageTextColor, stageVenue, stageRoom) in loadSettingsJson['stages']:
                self.stages.append(Stage.Stage(self.root, self.wcif, stageBackgroundColor, stageTextColor, stageVenue, stageRoom))
            self.cardText = loadSettingsJson['cardText']
            self.botToken = loadSettingsJson['botToken']
            self.botChannelId = loadSettingsJson['botChannelId']
        except:
            tkinter.messagebox.showerror(title='Settings Error !',
                                         message='Error in the Settings file, please make sure you selected the correct file and try to load again')
            return

        for stage in reversed(self.stages):
            stage.showStage()

        try:
            self.bot = TelegramBot.TelegramBot(self.botToken, self.botChannelId, True, False)
            self.bot.sendSimpleMessage('Bot interface ready')
        except:
            tkinter.messagebox.showerror(
                title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct, and the application isn\'t already running')
            return

    def updateCompIdCloseButton(self, compId, window):
        self.compId = compId
        try:
            self.reloadWCIF()
        except:
            tkinter.messagebox.showerror(
                title='Competition ID Error !', message='The WCIF was not found ! Please ensure that the competition ID is correct, you have access to the internet, and the WCA website is up')
        else:
            window.destroy()

    def updateCompId(self):
        compIdWindow = tk.Toplevel(self.root)
        compIdWindow.grab_set()
        compIdLabel = tk.Label(compIdWindow, text='Please enter competition ID to fetch the correct WCIF')
        compIdLabel.pack(padx=20, pady=5)
        compIdEntry = tk.Entry(compIdWindow, width=50)
        compIdEntry.insert(0, self.compId)
        compIdEntry.pack(padx=20, pady=5)
        compIdCloseButton = tk.Button(compIdWindow, text='Update and reload WCIF',
                                      command=lambda: self.updateCompIdCloseButton(compIdEntry.get(), compIdWindow))
        compIdCloseButton.pack(padx=20, pady=5)

    def reloadWCIF(self):
        jsonFile = urllib.request.urlopen(f'https://worldcubeassociation.org/api/v0/competitions/{self.compId}/wcif/public')
        self.wcif = json.loads(jsonFile.read())

    def updateMaxSeedCloseButton(self, maxSeed, window):
        try:
            self.maxSeed = int(maxSeed)
        except:
            tkinter.messagebox.showerror(title='Max Seed Error !', message='Error ! Please make sure the seed is a number')
        else:
            window.destroy()

    def updateMaxSeed(self):
        maxSeedWindow = tk.Toplevel(self.root)
        maxSeedWindow.grab_set()
        maxSeedLabel = tk.Label(maxSeedWindow, text='Please enter the maximum seed to be shown on stream')
        maxSeedLabel.pack(padx=20, pady=5)
        maxSeedEntry = tk.Entry(maxSeedWindow, width=20)
        maxSeedEntry.insert(0, self.maxSeed)
        maxSeedEntry.pack(padx=20, pady=5)
        maxSeedCloseButton = tk.Button(maxSeedWindow, text='Save max seed',
                                       command=lambda: self.updateMaxSeedCloseButton(maxSeedEntry.get(), maxSeedWindow))
        maxSeedCloseButton.pack(padx=20, pady=5)

    def stageSwitch(self, a, b, window, frame):
        oldStage = self.exampleStages[a]
        self.exampleStages[a] = self.exampleStages[b]
        self.exampleStages[b] = oldStage
        self.reloadStages(window, frame)

    def addStage(self, window, frame):
        venue = WCIFParse.getVenueId(self.wcif, WCIFParse.getVenues(self.wcif)[0])
        room = WCIFParse.getRoomId(self.wcif, venue, WCIFParse.getRooms(self.wcif, venue)[0])
        stage = Stage.Stage(self.root, self.wcif, '#FFFFFF', '#000000', venue, room)
        self.exampleStages.append(stage)
        stageWindow = stage.updateWindow(window, True)
        window.wait_window(stageWindow)
        self.reloadStages(window, frame)

    def editStage(self, window, frame, stage):
        stageWindow = stage.updateWindow(window, False)
        window.wait_window(stageWindow)
        self.reloadStages(window, frame)

    def deleteStage(self, window, frame, stage):
        self.exampleStages.remove(stage)
        self.reloadStages(window, frame)

    def reloadStages(self, window, frame):
        frame.grid_forget()
        frame.columnconfigure(0, pad=10)
        frame.columnconfigure(1, pad=10)
        frame.columnconfigure(2, pad=10)
        frame.columnconfigure(3, pad=10)
        frame.columnconfigure(4, pad=10)
        for widget in frame.winfo_children():
            widget.destroy()
        row = 0
        stageLabels = []
        stageUpButtons = []
        stageDownButtons = []
        stageEditButtons = []
        stageDeleteButtons = []
        for stage in self.exampleStages:
            stageLabels.append(tk.Label(
                frame, text=f'{WCIFParse.getVenueName(self.wcif, stage.venue)}, {WCIFParse.getRoomName(self.wcif, stage.venue, stage.room)}', fg=stage.textColor, bg=stage.backgroundColor))
            stageLabels[-1].grid(row=row, column=0)
            stageUpButtons.append(tk.Button(frame, text='↑', command=lambda a=row - 1, b=row: self.stageSwitch(a, b, window, frame)))
            stageUpButtons[-1].grid(row=row, column=1)
            if row == 0:
                stageUpButtons[-1]['state'] = 'disabled'
            stageDownButtons.append(tk.Button(frame, text='↓', command=lambda a=row, b=row + 1: self.stageSwitch(a, b, window, frame)))
            stageDownButtons[-1].grid(row=row, column=2)
            if row == len(self.exampleStages) - 1:
                stageDownButtons[-1]['state'] = 'disabled'
            stageEditButtons.append(tk.Button(frame, text='Edit', command=lambda localStage=stage: self.editStage(window, frame, localStage)))
            stageEditButtons[-1].grid(row=row, column=3)
            stageDeleteButtons.append(tk.Button(frame, text='Delete', command=lambda localStage=stage: self.deleteStage(window, frame, localStage)))
            stageDeleteButtons[-1].grid(row=row, column=4)
            row = row + 1
        frame.grid(row=1, column=0)

    def updateStagesCloseWindow(self, window):
        window.destroy()
        for stage in self.stages:
            stage.hideStage()
        self.stages = []
        for stage in self.exampleStages:
            self.stages.append(stage.copy())
        for stage in reversed(self.stages):
            stage.showStage()

    def updateStages(self):
        self.exampleStages = []
        for stage in self.stages:
            self.exampleStages.append(stage.copy())

        stagesWindow = tk.Toplevel(self.root)
        stagesWindow.grab_set()
        stagesWindow.rowconfigure(0, pad=10)
        stagesWindow.rowconfigure(1, pad=10)
        stagesWindow.rowconfigure(2, pad=10)
        stagesWindow.rowconfigure(3, pad=10)
        stagesLabel = tk.Label(
            stagesWindow, text='Update stages. You can assign a stage to any room (as declared on the WCA).\nMultiple stages can be assigned to the same room (if you didn\'t specify stages when making the schedule and assignments for example).')
        stagesLabel.grid(row=0, column=0)
        stagesFrame = tk.Frame(stagesWindow)
        self.reloadStages(stagesWindow, stagesFrame)
        addButton = tk.Button(stagesWindow, text='Add stage', command=lambda: self.addStage(stagesWindow, stagesFrame))
        addButton.grid(row=2, column=0)
        OKButton = tk.Button(stagesWindow, text='OK', command=lambda: self.updateStagesCloseWindow(stagesWindow))
        OKButton.grid(row=3, column=0)

    def updateCardTextCloseButton(self, cardText, window):
        self.cardText = cardText
        window.destroy()

    def updateCardText(self):
        cardTextWindow = tk.Toplevel(self.root)
        cardTextWindow.grab_set()
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
        cardTextLabel = tk.Label(cardTextWindow, text=cardTextDescription, justify='left')
        cardTextLabel.pack(padx=20, pady=5)
        cardTextEntry = tk.Text(cardTextWindow)
        cardTextEntry.insert('1.0', self.cardText)
        cardTextEntry.pack(padx=20, pady=5)
        cardTextCloseButton = tk.Button(cardTextWindow, text='Save card text',
                                        command=lambda: self.updateCardTextCloseButton(cardTextEntry.get('1.0', 'end-1c'), cardTextWindow))
        cardTextCloseButton.pack(padx=20, pady=5)

    def updateTelegramSettingsCloseButton(self, token, id, window):
        self.botToken = token
        self.botChannelId = id
        self.bot = TelegramBot.TelegramBot(token, id, True, False)
        self.bot.sendSimpleMessage('Bot Interface ready')
        window.destroy()

    def updateTelegramSettings(self):
        telegramWindow = tk.Toplevel(self.root)
        telegramWindow.grab_set()
        telegramLabel = tk.Label(telegramWindow, text='Please enter Telegram settings')
        telegramLabel.pack(pady=20)
        tokenLabel = tk.Label(telegramWindow, text='Interface bot token')
        tokenLabel.pack(pady=5)
        tokenEntry = tk.Entry(telegramWindow, width=50)
        tokenEntry.insert(0, self.botToken)
        tokenEntry.pack(pady=5)
        idLabel = tk.Label(telegramWindow, text='Channel ID between interface and card bots')
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
        compIdButton = tk.Button(frame, text='Update competition ID', command=self.updateCompId)
        compIdButton.grid(column=0, row=1)
        reloadButton = tk.Button(frame, text='Reload WCIF', command=self.reloadWCIF)
        reloadButton.grid(column=0, row=2)
        maxSeedButton = tk.Button(frame, text='Change Max Seed', command=self.updateMaxSeed)
        maxSeedButton.grid(column=0, row=3)
        stagesButton = tk.Button(frame, text='Setup stages', command=self.updateStages)
        stagesButton.grid(column=0, row=4)
        cardTextButton = tk.Button(frame, text='Change text on card', command=self.updateCardText)
        cardTextButton.grid(column=0, row=5)
        telegramButton = tk.Button(frame, text='Change Telegram Settings', command=self.updateTelegramSettings)
        telegramButton.grid(column=0, row=6)
        saveButton = tk.Button(frame, text='Save Settings...', command=self.saveSettings)
        saveButton.grid(column=0, row=7)
        saveButton = tk.Button(frame, text='Load Settings...', command=self.loadSettings)
        saveButton.grid(column=0, row=8)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
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
