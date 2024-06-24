import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk, font
from tkinter.colorchooser import askcolor
import json
import queue
import threading
import timeTowerUtils

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot, Image
from Common.commonUtils import cleverInt
import TimeTowerContent
import TimeTowerLine


class TimeTower:

    BG_COLOR = '#F4ECE1'

    def __init__(self, root):
        self.root = root
        self.compId = 0
        self.delay = 0
        self.region = 'World'
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.queueRound = queue.Queue()
        self.queueUpdate = queue.Queue()
        self.content = None
        self.bgLocalName = timeTowerUtils.DEFAULT_BG_LOCAL_NAME
        self.bgLocalResult = timeTowerUtils.DEFAULT_BG_LOCAL_RESULT
        self.bgForeignerName = timeTowerUtils.DEFAULT_BG_FOREIGNER_NAME
        self.bgForeignerResult = timeTowerUtils.DEFAULT_BG_FOREIGNER_RESULT
        self.widthRanking = timeTowerUtils.DEFAULT_WIDTH_RANKING
        self.widthFlagRectangle = timeTowerUtils.DEFAULT_WIDTH_FLAG_RECTANGLE
        self.heightFlag = timeTowerUtils.DEFAULT_HEIGHT_FLAG
        self.widthName = timeTowerUtils.DEFAULT_WIDTH_NAME
        self.widthFullName = timeTowerUtils.DEFAULT_WIDTH_FULL_NAME
        self.widthCount = timeTowerUtils.DEFAULT_WIDTH_COUNT
        self.widthResult = timeTowerUtils.DEFAULT_WIDTH_RESULT
        self.widthFullResult = timeTowerUtils.DEFAULT_WIDTH_FULL_RESULT
        self.fontFamily = timeTowerUtils.DEFAULT_FONT_FAMILY
        self.rankingSize = timeTowerUtils.DEFAULT_FONT_SIZE_BIG
        self.rankingModifiers = 'bold'
        self.nameSize = timeTowerUtils.DEFAULT_FONT_SIZE_BIG
        self.nameModifiers = 'bold'
        self.countSize = timeTowerUtils.DEFAULT_FONT_SIZE_BIG
        self.countModifiers = ''
        self.incompleteResultSize = timeTowerUtils.DEFAULT_FONT_SIZE_SMALL
        self.incompleteResultModifiers = 'italic'
        self.resultSize = timeTowerUtils.DEFAULT_FONT_SIZE_BIG
        self.resultModifiers = 'bold'
        self.fullResultSize = timeTowerUtils.DEFAULT_FONT_SIZE_SMALL
        self.fullResultModifiers = ''
        self.height = timeTowerUtils.DEFAULT_HEIGHT
        self.heightSeparator = timeTowerUtils.DEFAULT_HEIGHT_SEPARATOR
        self.colorLocalName = timeTowerUtils.DEFAULT_COLOR_LOCAL_NAME
        self.colorLocalResult = timeTowerUtils.DEFAULT_COLOR_LOCAL_RESULT
        self.colorForeignerName = timeTowerUtils.DEFAULT_COLOR_FOREIGNER_NAME
        self.colorForeignerResult = timeTowerUtils.DEFAULT_COLOR_FOREIGNER_RESULT
        self.maxNumber = timeTowerUtils.DEFAULT_MAX_NUMBER
        self.FPSX = timeTowerUtils.DEFAULT_FPS_X
        self.FPSY = timeTowerUtils.DEFAULT_FPS_Y
        self.durationX = timeTowerUtils.DEFAULT_DURATION_X
        self.durationY = timeTowerUtils.DEFAULT_DURATION_Y

        self.currentRow = 0
        self.rankingBoldVariable = None
        self.rankingItalicVariable = None
        self.nameBoldVariable = None
        self.nameItalicVariable = None
        self.countBoldVariable = None
        self.countItalicVariable = None
        self.incompleteResultBoldVariable = None
        self.incompleteResultItalicVariable = None
        self.resultBoldVariable = None
        self.resultItalicVariable = None
        self.fullResultBoldVariable = None
        self.fullResultItalicVariable = None
        self.exampleLines = []

        self.showSettingsFrame()

    def timeTowerEventCallback(self, message):

        messageSplit = message.split()
        event = messageSplit[0]
        number = int(messageSplit[1])

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

        result = timeTowerUtils.getQueryResult(query)
        for competitionEvent in result['competition']['competitionEvents']:
            if (competitionEvent['event']['id'] == event):
                for round in competitionEvent['rounds']:
                    if (round['number'] == number):
                        self.queueRound.put((int(round['id']), timeTowerUtils.CRITERIA[event]))
                        return

    def timeTowerExpandCallback(self, message):
        messageSplit = message.split()
        competitor = int(messageSplit[0])
        enable = messageSplit[1]
        for line in self.content.lines:
            if competitor == line.competitorRegistrantId:
                if enable == '1':
                    line.expandRequest = True
                else:
                    line.reduceRequest = True

    def loadContent(self):
        durationX = self.durationX / 1000
        durationY = self.durationY / 1000
        stepXmax = int(self.FPSX * self.durationX / 1000)
        stepYmax = int(self.FPSY * self.durationY / 1000)
        if self.content is None:
            self.content = TimeTowerContent.TimeTowerContent(self.root, self.queueRound, self.queueUpdate, self.region, self.bgLocalName, self.bgLocalResult, self.bgForeignerName, self.bgForeignerResult,
                                                             self.widthRanking, self.widthFlagRectangle, self.heightFlag, self.widthName, self.widthFullName, self.widthCount, self.widthResult, self.widthFullResult,
                                                             (self.fontFamily, self.rankingSize, self.rankingModifiers),
                                                             (self.fontFamily, self.nameSize, self.nameModifiers),
                                                             (self.fontFamily, self.countSize, self.countModifiers),
                                                             (self.fontFamily, self.incompleteResultSize, self.incompleteResultModifiers),
                                                             (self.fontFamily, self.resultSize, self.resultModifiers),
                                                             (self.fontFamily, self.fullResultSize, self.fullResultModifiers),
                                                             self.colorLocalName, self.colorLocalResult, self.colorForeignerName, self.colorForeignerResult,
                                                             self.height, self.heightSeparator, self.maxNumber, self.delay, stepXmax, stepYmax, durationX, durationY)
            self.content.showFrame()
            self.content.mainLoop()
        else:
            self.queueUpdate.put((self.region,
                                  self.widthRanking, self.widthFlagRectangle, self.heightFlag, self.widthName, self.widthFullName, self.widthCount, self.widthResult, self.widthFullResult,
                                  (self.fontFamily, self.rankingSize, self.rankingModifiers),
                                  (self.fontFamily, self.nameSize, self.nameModifiers),
                                  (self.fontFamily, self.countSize, self.countModifiers),
                                  (self.fontFamily, self.incompleteResultSize, self.incompleteResultModifiers),
                                  (self.fontFamily, self.resultSize, self.resultModifiers),
                                  (self.fontFamily, self.fullResultSize, self.fullResultModifiers),
                                  self.height, self.heightSeparator,
                                  self.bgLocalName, self.bgLocalResult,
                                  self.bgForeignerName, self.bgForeignerResult,
                                  self.colorLocalName, self.colorLocalResult,
                                  self.colorForeignerName, self.colorForeignerResult,
                                  self.maxNumber, self.delay, stepXmax, stepYmax, durationX, durationY))

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./', filetypes=(("JSON Files", "*.json"),
                                                    ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'compId': self.compId,
            'delay': self.delay,
            'region': self.region,
            'bgLocalName': self.bgLocalName,
            'bgLocalResult': self.bgLocalResult,
            'bgForeignerName': self.bgForeignerName,
            'bgForeignerResult': self.bgForeignerResult,
            'widthRanking': self.widthRanking,
            'widthFlagRectangle': self.widthFlagRectangle,
            'heightFlag': self.heightFlag,
            'widthName': self.widthName,
            'widthFullName': self.widthFullName,
            'widthCount': self.widthCount,
            'widthResult': self.widthResult,
            'widthFullResult': self.widthFullResult,
            'fontFamily': self.fontFamily,
            'rankingSize': self.rankingSize,
            'rankingModifiers': self.rankingModifiers,
            'nameSize': self.nameSize,
            'nameModifiers': self.nameModifiers,
            'countSize': self.countSize,
            'countModifiers': self.countModifiers,
            'incompleteResultSize': self.incompleteResultSize,
            'incompleteResultModifiers': self.incompleteResultModifiers,
            'resultSize': self.resultSize,
            'resultModifiers': self.resultModifiers,
            'fullResultSize': self.fullResultSize,
            'fullResultModifiers': self.fullResultModifiers,
            'height': self.height,
            'heightSeparator': self.heightSeparator,
            'colorLocalName': self.colorLocalName,
            'colorLocalResult': self.colorLocalResult,
            'colorForeignerName': self.colorForeignerName,
            'colorForeignerResult': self.colorForeignerResult,
            'durationX': self.durationX,
            'FPSX': self.FPSX,
            'durationY': self.durationY,
            'FPSY': self.FPSY,
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
            self.delay = loadSettingsJson['delay']
            self.region = loadSettingsJson['region']
            self.bgLocalName = loadSettingsJson['bgLocalName']
            self.bgLocalResult = loadSettingsJson['bgLocalResult']
            self.bgForeignerName = loadSettingsJson['bgForeignerName']
            self.bgForeignerResult = loadSettingsJson['bgForeignerResult']
            self.widthRanking = loadSettingsJson['widthRanking']
            self.widthFlagRectangle = loadSettingsJson['widthFlagRectangle']
            self.heightFlag = loadSettingsJson['heightFlag']
            self.widthName = loadSettingsJson['widthName']
            self.widthFullName = loadSettingsJson['widthFullName']
            self.widthCount = loadSettingsJson['widthCount']
            self.widthResult = loadSettingsJson['widthResult']
            self.widthFullResult = loadSettingsJson['widthFullResult']
            self.fontFamily = loadSettingsJson['fontFamily']
            self.rankingSize = loadSettingsJson['rankingSize']
            self.rankingModifiers = loadSettingsJson['rankingModifiers']
            self.nameSize = loadSettingsJson['nameSize']
            self.nameModifiers = loadSettingsJson['nameModifiers']
            self.countSize = loadSettingsJson['countSize']
            self.countModifiers = loadSettingsJson['countModifiers']
            self.incompleteResultSize = loadSettingsJson['incompleteResultSize']
            self.incompleteResultModifiers = loadSettingsJson['incompleteResultModifiers']
            self.resultSize = loadSettingsJson['resultSize']
            self.resultModifiers = loadSettingsJson['resultModifiers']
            self.fullResultSize = loadSettingsJson['fullResultSize']
            self.fullResultModifiers = loadSettingsJson['fullResultModifiers']
            self.height = loadSettingsJson['height']
            self.heightSeparator = loadSettingsJson['heightSeparator']
            self.colorLocalName = loadSettingsJson['colorLocalName']
            self.colorLocalResult = loadSettingsJson['colorLocalResult']
            self.colorForeignerName = loadSettingsJson['colorForeignerName']
            self.colorForeignerResult = loadSettingsJson['colorForeignerResult']
            self.durationX = loadSettingsJson['durationX']
            self.FPSX = loadSettingsJson['FPSX']
            self.durationY = loadSettingsJson['durationY']
            self.FPSY = loadSettingsJson['FPSY']
            self.botToken = loadSettingsJson['botToken']
            self.botChannelId = loadSettingsJson['botChannelId']
        except:
            tkinter.messagebox.showerror(title='Settings Error !',
                                         message='Error in the Settings file, please make sure you selected the correct file and try to load again')
            return
        try:
            if self.bot is None:
                self.bot = TelegramBot.TelegramBot(self.botToken, self.botChannelId, False, True)
                self.bot.sendSimpleMessage('Bot TimeTower ready')
                self.bot.setMessageHandler(['timeTowerEvent'], self.timeTowerEventCallback)
                self.bot.setMessageHandler(['timeTowerExpand'], self.timeTowerExpandCallback)
                self.threadBot = threading.Thread(target=self.bot.startPolling)
                self.threadBot.daemon = True
                self.threadBot.start()
        except:
            tkinter.messagebox.showerror(
                title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct')
            return

        roundId = 0
        criteria = ''
        self.loadContent()

    def updateCompIdCloseButton(self, compId, window):
        try:
            self.compId = int(compId)
        except:
            tkinter.messagebox.showerror(title='Competition ID Error !',
                                         message='The ID must be a number! This is the WCA Live ID, not the WCA competition ID.')
        else:
            window.destroy()

    def updateCompId(self):
        compIdWindow = tk.Toplevel(self.root)
        compIdWindow.grab_set()
        compIdLabel = tk.Label(
            compIdWindow, text='Please enter competition ID to fetch the correct WCIF\nThis is NOT the WCA ID but the Live ID (4 digits)')
        compIdLabel.pack(padx=20, pady=5)
        compIdEntry = tk.Entry(compIdWindow, width=50)
        compIdEntry.insert(0, self.compId)
        compIdEntry.pack(padx=20, pady=5)
        compIdCloseButton = tk.Button(compIdWindow, text='Update ID', command=lambda: self.updateCompIdCloseButton(compIdEntry.get(), compIdWindow))
        compIdCloseButton.pack(padx=20, pady=5)

    def updateDelayCloseButton(self, delay, window):
        try:
            self.delay = int(delay)
        except:
            tkinter.messagebox.showerror(title='Delay Error !', message='The delay must be a whole number ! (No units needed)')
        else:
            self.loadContent()
            window.destroy()

    def updateDelay(self):
        delayWindow = tk.Toplevel(self.root)
        delayWindow.grab_set()
        delayLabel = tk.Label(
            delayWindow, text='Please enter the delay (in ms) between 2 consecutive fetches to Live.\nPlease take into account that this does NOT include the time needed to retrieve data from Live and display it.')
        delayLabel.pack(padx=20, pady=5)
        delayEntry = tk.Entry(delayWindow, width=50)
        delayEntry.insert(0, self.delay)
        delayEntry.pack(padx=20, pady=5)
        delayCloseButton = tk.Button(delayWindow, text='Update delay', command=lambda: self.updateDelayCloseButton(delayEntry.get(), delayWindow))
        delayCloseButton.pack(padx=20, pady=5)

    def checkRegionSeparator(self, regionBox):
        if regionBox.get() == timeTowerUtils.SEPARATOR:
            regionBox.set('World')

    def updateRegionCloseButton(self, region, window):
        self.region = region
        self.loadContent()
        window.destroy()

    def updateRegion(self):
        regionWindow = tk.Toplevel(self.root)
        regionWindow.grab_set()
        regionLabel = tk.Label(
            regionWindow, text='Please choose a region (country or continent) if you want local competitors to be highlighted, so you can see the local results more easily.\nThe "World" option highlights everyone the same.')
        regionLabel.pack(padx=20, pady=5)
        regionBox = ttk.Combobox(regionWindow)
        regionBox['values'] = timeTowerUtils.REGION_OPTIONS
        regionBox.set(self.region)
        regionBox['state'] = 'readonly'
        regionBox.bind('<<ComboboxSelected>>', lambda event: self.checkRegionSeparator(regionBox))
        regionBox.pack(padx=20, pady=5)
        regionCloseButton = tk.Button(regionWindow, text='Update region',
                                      command=lambda: self.updateRegionCloseButton(regionBox.get(), regionWindow))
        regionCloseButton.pack(padx=20, pady=5)

    def layoutEndRow(self, frame, pad):
        frame.rowconfigure(self.currentRow, pad=pad)
        self.currentRow = self.currentRow + 1

    def createExampleLines(self, window):
        self.exampleCanvas = tk.Canvas(window, width=timeTowerUtils.LAYOUT_CANVAS_WIDTH,
                                       height=timeTowerUtils.LAYOUT_CANVAS_HEIGHT, bg='#FFF')
        self.exampleCanvas.pack(pady=5)
        self.exampleLines = []
        self.exampleLines.append(TimeTowerLine.TimeTowerLine(self.exampleCanvas, self.bgLocalName, self.bgLocalResult,
                                                             self.widthRanking, self.widthFlagRectangle, self.heightFlag, self.widthName, self.widthFullName, self.widthCount, self.widthResult, self.widthFullResult,
                                                             (self.fontFamily, self.rankingSize, self.rankingModifiers),
                                                             (self.fontFamily, self.nameSize, self.nameModifiers),
                                                             (self.fontFamily, self.countSize, self.countModifiers),
                                                             (self.fontFamily, self.incompleteResultSize, self.incompleteResultModifiers),
                                                             (self.fontFamily, self.resultSize, self.resultModifiers),
                                                             (self.fontFamily, self.fullResultSize, self.fullResultModifiers),
                                                             self.colorLocalName, self.colorLocalResult, self.height, self.heightSeparator, 0, 0, 0, 'PL', 'Tymon Kolasiński', 'average', 1, 1))
        self.exampleLines.append(TimeTowerLine.TimeTowerLine(self.exampleCanvas, self.bgForeignerName, self.bgForeignerResult,
                                                             self.widthRanking, self.widthFlagRectangle, self.heightFlag, self.widthName, self.widthFullName, self.widthCount, self.widthResult, self.widthFullResult,
                                                             (self.fontFamily, self.rankingSize, self.rankingModifiers),
                                                             (self.fontFamily, self.nameSize, self.nameModifiers),
                                                             (self.fontFamily, self.countSize, self.countModifiers),
                                                             (self.fontFamily, self.incompleteResultSize, self.incompleteResultModifiers),
                                                             (self.fontFamily, self.resultSize, self.resultModifiers),
                                                             (self.fontFamily, self.fullResultSize, self.fullResultModifiers),
                                                             self.colorForeignerName, self.colorForeignerResult, self.height, self.heightSeparator, 0, 0, 0, 'US', 'Max Park', 'average', 1, 1))
        self.exampleLines[0].ranking = 1
        self.exampleLines[0].nextRanking = 1
        self.exampleLines[0].results = [500, 600, 700, 800, timeTowerUtils.DNF_ATTEMPT]
        self.exampleLines[0].currentResult = 700
        self.exampleLines[0].expanded = True
        self.exampleLines[1].ranking = 2
        self.exampleLines[1].nextRanking = 2
        self.exampleLines[1].results = [0, 0, 0, 0]
        self.exampleLines[1].currentResult = 500
        for line in self.exampleLines:
            line.showLine(0, 0)

    def updateExampleLines(self, widthRanking=None, widthFlagRectangle=None, heightFlag=None, widthName=None, widthFullName=None, widthCount=None, widthResult=None, widthFullResult=None, height=None, heightSeparator=None, bgLocalName=None, bgLocalResult=None, bgForeignerName=None, bgForeignerResult=None, fontRanking=None, fontName=None, fontCount=None, fontIncompleteResult=None, fontResult=None, fontFullResult=None, colorLocalName=None, colorLocalResult=None, colorForeignerName=None, colorForeignerResult=None):
        for line in self.exampleLines:
            if widthRanking is not None:
                line.widthRanking = widthRanking
            if widthFlagRectangle is not None:
                line.widthFlagRectangle = widthFlagRectangle
            if heightFlag is not None:
                line.heightFlag = heightFlag
                line.flagImage = Image.getFlag(heightFlag, line.country)
            if widthName is not None:
                line.widthName = widthName
            if widthFullName is not None:
                line.widthFullName = widthFullName
            if widthCount is not None:
                line.widthCount = widthCount
            if widthResult is not None:
                line.widthResult = widthResult
            if widthFullResult is not None:
                line.widthFullResult = widthFullResult
            if height is not None:
                line.height = height
            if heightSeparator is not None:
                line.heightSeparator = heightSeparator
            if fontRanking is not None:
                line.fontRanking = fontRanking
            if fontName is not None:
                line.fontName = fontName
            if fontCount is not None:
                line.fontCount = fontCount
            if fontIncompleteResult is not None:
                line.fontIncompleteResult = fontIncompleteResult
            if fontResult is not None:
                line.fontResult = fontResult
            if fontFullResult is not None:
                line.fontFullResult = fontFullResult
        if bgLocalName is not None:
            self.exampleLines[0].bgName = bgLocalName
        if bgLocalResult is not None:
            self.exampleLines[0].bgResult = bgLocalResult
        if bgForeignerName is not None:
            self.exampleLines[1].bgName = bgForeignerName
        if bgForeignerResult is not None:
            self.exampleLines[1].bgResult = bgForeignerResult
        if colorLocalName is not None:
            self.exampleLines[0].colorName = colorLocalName
        if colorLocalResult is not None:
            self.exampleLines[0].colorResult = colorLocalResult
        if colorForeignerName is not None:
            self.exampleLines[1].colorName = colorForeignerName
        if colorForeignerResult is not None:
            self.exampleLines[1].colorResult = colorForeignerResult

        self.exampleCanvas.delete('all')
        for line in self.exampleLines:
            line.showLine(0, 0)

    def updateColorButton(self, variable):
        colors = askcolor(variable.get(), title='Pick a color')
        if colors[1] is not None:
            variable.set(colors[1])

    def updateLayoutCloseButton(self, widthRanking, widthFlagRectangle, heightFlag, widthName, widthFullName, widthCount, widthResult, widthFullResult, height, heightSeparator, fontFamily, rankingSize, rankingModifiers, nameSize, nameModifiers, countSize, countModifiers, incompleteResultSize, incompleteResultModifiers, resultSize, resultModifiers, fullResultSize, fullResultModifiers, bgLocalName, bgLocalResult, bgForeignerName, bgForeignerResult, colorLocalName, colorLocalResult, colorForeignerName, colorForeignerResult, durationX, FPSX, durationY, FPSY, window):
        try:
            self.widthRanking = widthRanking
            self.widthFlagRectangle = widthFlagRectangle
            self.heightFlag = heightFlag
            self.widthName = widthName
            self.widthFullName = widthFullName
            self.widthCount = widthCount
            self.widthResult = widthResult
            self.widthFullResult = widthFullResult
            self.height = height
            self.heightSeparator = heightSeparator
            self.fontFamily = fontFamily
            self.rankingSize = rankingSize
            self.rankingModifiers = rankingModifiers
            self.nameSize = nameSize
            self.nameModifiers = nameModifiers
            self.countSize = countSize
            self.countModifiers = countModifiers
            self.incompleteResultSize = incompleteResultSize
            self.incompleteResultModifiers = incompleteResultModifiers
            self.resultSize = resultSize
            self.resultModifiers = resultModifiers
            self.fullResultSize = fullResultSize
            self.fullResultModifiers = fullResultModifiers
            self.bgLocalName = bgLocalName
            self.bgLocalResult = bgLocalResult
            self.bgForeignerName = bgForeignerName
            self.bgForeignerResult = bgForeignerResult
            self.colorLocalName = colorLocalName
            self.colorLocalResult = colorLocalResult
            self.colorForeignerName = colorForeignerName
            self.colorForeignerResult = colorForeignerResult
            self.durationX = durationX
            self.FPSX = FPSX
            self.durationY = durationY
            self.FPSY = FPSY
        except:
            tkinter.messagebox.showerror(title='Layout Settings Error !', message='Error in the settings! Please check all values.')
        else:
            self.loadContent()
            window.destroy()

    def updateLayout(self):
        layoutWindow = tk.Toplevel(self.root)
        layoutWindow.grab_set()

        layoutLabel = tk.Label(layoutWindow, text='Customize the tower layout with the following tabs:')
        layoutLabel.pack(pady=5)

        layoutNotebook = ttk.Notebook(layoutWindow)
        layoutNotebook.pack(pady=5)

        # Size

        sizeFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(sizeFrame, text='Size')
        sizeFrame.columnconfigure(0, weight=1)
        sizeFrame.columnconfigure(1, weight=1)
        self.currentRow = 0
        emptyFrames = []

        widthRankingLabel = tk.Label(sizeFrame, text='Ranking width:')
        widthRankingLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthRankingVariable = tk.StringVar()
        widthRankingSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH, textvariable=widthRankingVariable)
        widthRankingSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthRankingVariable.set(f'{self.widthRanking}')

        self.layoutEndRow(sizeFrame, 10)
        emptyFrames.append(tk.Frame(sizeFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(sizeFrame, 30)

        flagLabel = tk.Label(sizeFrame, text='The flag width will adjust to the given height to keep the flag\'s ratio.\nThe "Flag container width" should be big enough to contain any flag, and allows you to have some padding on the sides of the flag.')
        flagLabel.grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(sizeFrame, 10)

        widthFlagRectangleLabel = tk.Label(sizeFrame, text='Flag container width:')
        widthFlagRectangleLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthFlagRectangleVariable = tk.StringVar()
        widthFlagRectangleSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH,
                                               textvariable=widthFlagRectangleVariable)
        widthFlagRectangleSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthFlagRectangleVariable.set(f'{self.widthFlagRectangle}')
        self.layoutEndRow(sizeFrame, 10)

        heightFlagLabel = tk.Label(sizeFrame, text='Flag height:')
        heightFlagLabel.grid(column=0, row=self.currentRow, sticky='e')
        heightFlagVariable = tk.StringVar()
        heightFlagSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH, textvariable=heightFlagVariable)
        heightFlagSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        heightFlagVariable.set(f'{self.heightFlag}')

        self.layoutEndRow(sizeFrame, 10)
        emptyFrames.append(tk.Frame(sizeFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(sizeFrame, 30)

        widthNameLabel = tk.Label(sizeFrame, text='Abbreviated name width:')
        widthNameLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthNameVariable = tk.StringVar()
        widthNameSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH, textvariable=widthNameVariable)
        widthNameSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthNameVariable.set(f'{self.widthName}')
        self.layoutEndRow(sizeFrame, 10)

        widthFullNameLabel = tk.Label(sizeFrame, text='Full name width:')
        widthFullNameLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthFullNameVariable = tk.StringVar()
        widthFullNameSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_EXTENDED_WIDTH,
                                          textvariable=widthFullNameVariable)
        widthFullNameSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthFullNameVariable.set(f'{self.widthFullName}')

        self.layoutEndRow(sizeFrame, 10)
        emptyFrames.append(tk.Frame(sizeFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(sizeFrame, 30)

        widthCountLabel = tk.Label(sizeFrame, text='Solve count width:')
        widthCountLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthCountVariable = tk.StringVar()
        widthCountSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH, textvariable=widthCountVariable)
        widthCountSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthCountVariable.set(f'{self.widthCount}')
        self.layoutEndRow(sizeFrame, 10)

        widthResultLabel = tk.Label(sizeFrame, text='Result width:')
        widthResultLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthResultVariable = tk.StringVar()
        widthResultSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH, textvariable=widthResultVariable)
        widthResultSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthResultVariable.set(f'{self.widthResult}')
        self.layoutEndRow(sizeFrame, 10)

        widthFullResultLabel = tk.Label(sizeFrame, text='Full results width:')
        widthFullResultLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthFullResultVariable = tk.StringVar()
        widthFullResultSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_EXTENDED_WIDTH,
                                            textvariable=widthFullResultVariable)
        widthFullResultSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthFullResultVariable.set(f'{self.widthFullResult}')

        self.layoutEndRow(sizeFrame, 10)
        emptyFrames.append(tk.Frame(sizeFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(sizeFrame, 30)

        heightLabel = tk.Label(sizeFrame, text='Line height:')
        heightLabel.grid(column=0, row=self.currentRow, sticky='e')
        heightVariable = tk.StringVar()
        heightSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_HEIGHT, textvariable=heightVariable)
        heightSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        heightVariable.set(f'{self.height}')
        self.layoutEndRow(sizeFrame, 10)

        heightSeparatorLabel = tk.Label(sizeFrame, text='Height between lines:')
        heightSeparatorLabel.grid(column=0, row=self.currentRow, sticky='e')
        heightSeparatorVariable = tk.StringVar()
        heightSeparatorSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_HEIGHT, textvariable=heightSeparatorVariable)
        heightSeparatorSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        heightSeparatorVariable.set(f'{self.heightSeparator}')
        self.layoutEndRow(sizeFrame, 10)

        widthRankingVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthRanking=cleverInt(widthRankingVariable.get())))
        widthFlagRectangleVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthFlagRectangle=cleverInt(widthFlagRectangleVariable.get())))
        heightFlagVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            heightFlag=cleverInt(heightFlagVariable.get())))
        widthNameVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthName=cleverInt(widthNameVariable.get())))
        widthFullNameVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthFullName=cleverInt(widthFullNameVariable.get())))
        widthCountVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthCount=cleverInt(widthCountVariable.get())))
        widthResultVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthResult=cleverInt(widthResultVariable.get())))
        widthFullResultVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            widthFullResult=cleverInt(widthFullResultVariable.get())))
        heightVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            height=cleverInt(heightVariable.get())))
        heightSeparatorVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            heightSeparator=cleverInt(heightSeparatorVariable.get())))

        # Font

        fontFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(fontFrame, text='Fonts')
        fontFrame.columnconfigure(0, weight=1)
        fontFrame.columnconfigure(1, weight=1)
        self.currentRow = 0
        emptyFrames = []

        fonts = list(font.families())
        fonts.sort()

        layoutLabel = tk.Label(fontFrame, text='Customize the tower fonts')
        layoutLabel.grid(column=0, columnspan=2, row=self.currentRow)

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 30)

        fontFamilyLabel = tk.Label(fontFrame, text='Font:')
        fontFamilyLabel.grid(column=0, row=self.currentRow, sticky='e')
        fontFamilyVariable = tk.StringVar()
        fontFamilyMenu = ttk.Combobox(fontFrame, textvariable=fontFamilyVariable)
        fontFamilyMenu['values'] = fonts
        fontFamilyVariable.set(self.fontFamily)
        fontFamilyMenu.set(self.fontFamily)
        fontFamilyMenu['state'] = 'readonly'
        fontFamilyMenu.grid(column=1, row=self.currentRow, sticky='w')

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 10)

        rankingSizeLabel = tk.Label(fontFrame, text='Ranking text size:')
        rankingSizeLabel.grid(column=0, row=self.currentRow, sticky='e')
        rankingSizeVariable = tk.StringVar()
        rankingSizeSpinbox = tk.Spinbox(fontFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_FONT, textvariable=rankingSizeVariable)
        rankingSizeSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        rankingSizeVariable.set(f'{self.rankingSize}')
        self.layoutEndRow(fontFrame, 10)

        self.rankingBoldVariable = tk.BooleanVar()
        rankingBoldCheckbox = tk.Checkbutton(fontFrame, text='Bold', variable=self.rankingBoldVariable)
        rankingBoldCheckbox.grid(column=0, row=self.currentRow, sticky='e')
        self.rankingItalicVariable = tk.BooleanVar()
        rankingItalicCheckbox = tk.Checkbutton(fontFrame, text='Italic', variable=self.rankingItalicVariable)
        rankingItalicCheckbox.grid(column=1, row=self.currentRow, sticky='w')
        timeTowerUtils.setModifiersVariables(self.rankingModifiers, self.rankingBoldVariable, self.rankingItalicVariable)

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 10)

        nameSizeLabel = tk.Label(fontFrame, text='Name text size:')
        nameSizeLabel.grid(column=0, row=self.currentRow, sticky='e')
        nameSizeVariable = tk.StringVar()
        nameSizeSpinbox = tk.Spinbox(fontFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_FONT, textvariable=nameSizeVariable)
        nameSizeSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        nameSizeVariable.set(f'{self.nameSize}')
        self.layoutEndRow(fontFrame, 10)

        self.nameBoldVariable = tk.BooleanVar()
        nameBoldCheckbox = tk.Checkbutton(fontFrame, text='Bold', variable=self.nameBoldVariable)
        nameBoldCheckbox.grid(column=0, row=self.currentRow, sticky='e')
        self.nameItalicVariable = tk.BooleanVar()
        nameItalicCheckbox = tk.Checkbutton(fontFrame, text='Italic', variable=self.nameItalicVariable)
        nameItalicCheckbox.grid(column=1, row=self.currentRow, sticky='w')
        timeTowerUtils.setModifiersVariables(self.nameModifiers, self.nameBoldVariable, self.nameItalicVariable)

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 10)

        countSizeLabel = tk.Label(fontFrame, text='Solves count text size:')
        countSizeLabel.grid(column=0, row=self.currentRow, sticky='e')
        countSizeVariable = tk.StringVar()
        countSizeSpinbox = tk.Spinbox(fontFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_FONT, textvariable=countSizeVariable)
        countSizeSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        countSizeVariable.set(f'{self.countSize}')
        self.layoutEndRow(fontFrame, 10)

        self.countBoldVariable = tk.BooleanVar()
        countBoldCheckbox = tk.Checkbutton(fontFrame, text='Bold', variable=self.countBoldVariable)
        countBoldCheckbox.grid(column=0, row=self.currentRow, sticky='e')
        self.countItalicVariable = tk.BooleanVar()
        countItalicCheckbox = tk.Checkbutton(fontFrame, text='Italic', variable=self.countItalicVariable)
        countItalicCheckbox.grid(column=1, row=self.currentRow, sticky='w')
        timeTowerUtils.setModifiersVariables(self.countModifiers, self.countBoldVariable, self.countItalicVariable)

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 10)

        incompleteResultSizeLabel = tk.Label(fontFrame, text='Incomplete result text size:')
        incompleteResultSizeLabel.grid(column=0, row=self.currentRow, sticky='e')
        incompleteResultSizeVariable = tk.StringVar()
        incompleteResultSizeSpinbox = tk.Spinbox(fontFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_FONT,
                                                 textvariable=incompleteResultSizeVariable)
        incompleteResultSizeSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        incompleteResultSizeVariable.set(f'{self.incompleteResultSize}')
        self.layoutEndRow(fontFrame, 10)

        self.incompleteResultBoldVariable = tk.BooleanVar()
        incompleteResultBoldCheckbox = tk.Checkbutton(fontFrame, text='Bold', variable=self.incompleteResultBoldVariable)
        incompleteResultBoldCheckbox.grid(column=0, row=self.currentRow, sticky='e')
        self.incompleteResultItalicVariable = tk.BooleanVar()
        incompleteResultItalicCheckbox = tk.Checkbutton(fontFrame, text='Italic', variable=self.incompleteResultItalicVariable)
        incompleteResultItalicCheckbox.grid(column=1, row=self.currentRow, sticky='w')
        timeTowerUtils.setModifiersVariables(self.incompleteResultModifiers, self.incompleteResultBoldVariable, self.incompleteResultItalicVariable)

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 10)

        resultSizeLabel = tk.Label(fontFrame, text='Result text size:')
        resultSizeLabel.grid(column=0, row=self.currentRow, sticky='e')
        resultSizeVariable = tk.StringVar()
        resultSizeSpinbox = tk.Spinbox(fontFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_FONT, textvariable=resultSizeVariable)
        resultSizeSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        resultSizeVariable.set(f'{self.resultSize}')
        self.layoutEndRow(fontFrame, 10)

        self.resultBoldVariable = tk.BooleanVar()
        resultBoldCheckbox = tk.Checkbutton(fontFrame, text='Bold', variable=self.resultBoldVariable)
        resultBoldCheckbox.grid(column=0, row=self.currentRow, sticky='e')
        self.resultItalicVariable = tk.BooleanVar()
        resultItalicCheckbox = tk.Checkbutton(fontFrame, text='Italic', variable=self.resultItalicVariable)
        resultItalicCheckbox.grid(column=1, row=self.currentRow, sticky='w')
        timeTowerUtils.setModifiersVariables(self.resultModifiers, self.resultBoldVariable, self.resultItalicVariable)

        self.layoutEndRow(fontFrame, 10)
        emptyFrames.append(tk.Frame(fontFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(fontFrame, 10)

        fullResultSizeLabel = tk.Label(fontFrame, text='Full result text size:')
        fullResultSizeLabel.grid(column=0, row=self.currentRow, sticky='e')
        fullResultSizeVariable = tk.StringVar()
        fullResultSizeSpinbox = tk.Spinbox(fontFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_FONT, textvariable=fullResultSizeVariable)
        fullResultSizeSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        fullResultSizeVariable.set(f'{self.fullResultSize}')
        self.layoutEndRow(fontFrame, 10)

        self.fullResultBoldVariable = tk.BooleanVar()
        fullResultBoldCheckbox = tk.Checkbutton(fontFrame, text='Bold', variable=self.fullResultBoldVariable)
        fullResultBoldCheckbox.grid(column=0, row=self.currentRow, sticky='e')
        self.fullResultItalicVariable = tk.BooleanVar()
        fullResultItalicCheckbox = tk.Checkbutton(fontFrame, text='Italic', variable=self.fullResultItalicVariable)
        fullResultItalicCheckbox.grid(column=1, row=self.currentRow, sticky='w')
        timeTowerUtils.setModifiersVariables(self.fullResultModifiers, self.fullResultBoldVariable, self.fullResultItalicVariable)

        fontFamilyVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontRanking=(fontFamilyVariable.get(), cleverInt(rankingSizeVariable.get()),
                         timeTowerUtils.getModifiers(self.rankingBoldVariable.get(), self.rankingItalicVariable.get())),
            fontName=(fontFamilyVariable.get(), cleverInt(nameSizeVariable.get()),
                      timeTowerUtils.getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get())),
            fontCount=(fontFamilyVariable.get(), cleverInt(countSizeVariable.get()),
                       timeTowerUtils.getModifiers(self.countBoldVariable.get(), self.countItalicVariable.get())),
            fontIncompleteResult=(fontFamilyVariable.get(), cleverInt(incompleteResultSizeVariable.get()),
                                  timeTowerUtils.getModifiers(self.incompleteResultBoldVariable.get(), self.incompleteResultItalicVariable.get())),
            fontResult=(fontFamilyVariable.get(), cleverInt(resultSizeVariable.get()),
                        timeTowerUtils.getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get())),
            fontFullResult=(fontFamilyVariable.get(), cleverInt(fullResultSizeVariable.get()),
                            timeTowerUtils.getModifiers(self.fullResultBoldVariable.get(), self.fullResultItalicVariable.get()))))
        rankingSizeVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontRanking=(fontFamilyVariable.get(), cleverInt(rankingSizeVariable.get()), timeTowerUtils.getModifiers(self.rankingBoldVariable.get(), self.rankingItalicVariable.get()))))
        self.rankingBoldVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontRanking=(fontFamilyVariable.get(), cleverInt(rankingSizeVariable.get()), timeTowerUtils.getModifiers(self.rankingBoldVariable.get(), self.rankingItalicVariable.get()))))
        self.rankingItalicVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontRanking=(fontFamilyVariable.get(), cleverInt(rankingSizeVariable.get()), timeTowerUtils.getModifiers(self.rankingBoldVariable.get(), self.rankingItalicVariable.get()))))
        nameSizeVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontName=(fontFamilyVariable.get(), cleverInt(nameSizeVariable.get()), timeTowerUtils.getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        self.nameBoldVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontName=(fontFamilyVariable.get(), cleverInt(nameSizeVariable.get()), timeTowerUtils.getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        self.nameItalicVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontName=(fontFamilyVariable.get(), cleverInt(nameSizeVariable.get()), timeTowerUtils.getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        countSizeVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontCount=(fontFamilyVariable.get(), cleverInt(countSizeVariable.get()), timeTowerUtils.getModifiers(self.countBoldVariable.get(), self.countItalicVariable.get()))))
        self.countBoldVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontCount=(fontFamilyVariable.get(), cleverInt(countSizeVariable.get()), timeTowerUtils.getModifiers(self.countBoldVariable.get(), self.countItalicVariable.get()))))
        self.countItalicVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontCount=(fontFamilyVariable.get(), cleverInt(countSizeVariable.get()), timeTowerUtils.getModifiers(self.countBoldVariable.get(), self.countItalicVariable.get()))))
        incompleteResultSizeVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontIncompleteResult=(fontFamilyVariable.get(), cleverInt(incompleteResultSizeVariable.get()), timeTowerUtils.getModifiers(self.incompleteResultBoldVariable.get(), self.incompleteResultItalicVariable.get()))))
        self.incompleteResultBoldVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontIncompleteResult=(fontFamilyVariable.get(), cleverInt(incompleteResultSizeVariable.get()), timeTowerUtils.getModifiers(self.incompleteResultBoldVariable.get(), self.incompleteResultItalicVariable.get()))))
        self.incompleteResultItalicVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontIncompleteResult=(fontFamilyVariable.get(), cleverInt(incompleteResultSizeVariable.get()), timeTowerUtils.getModifiers(self.incompleteResultBoldVariable.get(), self.incompleteResultItalicVariable.get()))))
        resultSizeVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontResult=(fontFamilyVariable.get(), cleverInt(resultSizeVariable.get()), timeTowerUtils.getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        self.resultBoldVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontResult=(fontFamilyVariable.get(), cleverInt(resultSizeVariable.get()), timeTowerUtils.getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        self.resultItalicVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontResult=(fontFamilyVariable.get(), cleverInt(resultSizeVariable.get()), timeTowerUtils.getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        fullResultSizeVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontFullResult=(fontFamilyVariable.get(), cleverInt(fullResultSizeVariable.get()), timeTowerUtils.getModifiers(self.fullResultBoldVariable.get(), self.fullResultItalicVariable.get()))))
        self.fullResultBoldVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontFullResult=(fontFamilyVariable.get(), cleverInt(fullResultSizeVariable.get()), timeTowerUtils.getModifiers(self.fullResultBoldVariable.get(), self.fullResultItalicVariable.get()))))
        self.fullResultItalicVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            fontFullResult=(fontFamilyVariable.get(), cleverInt(fullResultSizeVariable.get()), timeTowerUtils.getModifiers(self.fullResultBoldVariable.get(), self.fullResultItalicVariable.get()))))

        # Colors

        colorFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(colorFrame, text='Colors')
        colorFrame.columnconfigure(0, weight=1)
        colorFrame.columnconfigure(1, weight=1)
        self.currentRow = 0
        emptyFrames = []

        colorLabel = tk.Label(colorFrame, text='Customize the colors')
        colorLabel.grid(column=0, columnspan=2, row=self.currentRow)

        self.layoutEndRow(colorFrame, 10)
        emptyFrames.append(tk.Frame(colorFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(colorFrame, 30)

        localColorLabel = tk.Label(colorFrame, text='Local competitors:')
        localColorLabel.grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(colorFrame, 10)

        bgLocalNameVariable = tk.StringVar()
        bgLocalNameVariable.set(self.bgLocalName)
        bgLocalNameButton = tk.Button(colorFrame, text='Local name background', command=lambda: self.updateColorButton(bgLocalNameVariable))
        bgLocalNameButton.grid(column=0, row=self.currentRow, sticky='e')
        colorLocalNameVariable = tk.StringVar()
        colorLocalNameVariable.set(self.colorLocalName)
        colorLocalNameButton = tk.Button(colorFrame, text='Local name text color', command=lambda: self.updateColorButton(colorLocalNameVariable))
        colorLocalNameButton.grid(column=1, row=self.currentRow, sticky='w')
        self.layoutEndRow(colorFrame, 10)

        bgLocalResultVariable = tk.StringVar()
        bgLocalResultVariable.set(self.bgLocalResult)
        bgLocalResultButton = tk.Button(colorFrame, text='Local results background', command=lambda: self.updateColorButton(bgLocalResultVariable))
        bgLocalResultButton.grid(column=0, row=self.currentRow, sticky='e')
        colorLocalResultVariable = tk.StringVar()
        colorLocalResultVariable.set(self.colorLocalResult)
        colorLocalResultButton = tk.Button(colorFrame, text='Local results text color',
                                           command=lambda: self.updateColorButton(colorLocalResultVariable))
        colorLocalResultButton.grid(column=1, row=self.currentRow, sticky='w')

        self.layoutEndRow(colorFrame, 10)
        emptyFrames.append(tk.Frame(colorFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(colorFrame, 30)

        localColorLabel = tk.Label(colorFrame, text='Foreign competitors:')
        localColorLabel.grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(colorFrame, 10)

        bgForeignerNameVariable = tk.StringVar()
        bgForeignerNameVariable.set(self.bgForeignerName)
        bgForeignerNameButton = tk.Button(colorFrame, text='Foreigner name background',
                                          command=lambda: self.updateColorButton(bgForeignerNameVariable))
        bgForeignerNameButton.grid(column=0, row=self.currentRow, sticky='e')
        colorForeignerNameVariable = tk.StringVar()
        colorForeignerNameVariable.set(self.colorForeignerName)
        colorForeignerNameButton = tk.Button(colorFrame, text='Foreigner name text color',
                                             command=lambda: self.updateColorButton(colorForeignerNameVariable))
        colorForeignerNameButton.grid(column=1, row=self.currentRow, sticky='w')
        self.layoutEndRow(colorFrame, 10)

        bgForeignerResultVariable = tk.StringVar()
        bgForeignerResultVariable.set(self.bgForeignerResult)
        bgForeignerResultButton = tk.Button(colorFrame, text='Foreigner results background',
                                            command=lambda: self.updateColorButton(bgForeignerResultVariable))
        bgForeignerResultButton.grid(column=0, row=self.currentRow, sticky='e')
        colorForeignerResultVariable = tk.StringVar()
        colorForeignerResultVariable.set(self.colorForeignerResult)
        colorForeignerResultButton = tk.Button(colorFrame, text='Foreigner results text color',
                                               command=lambda: self.updateColorButton(colorForeignerResultVariable))
        colorForeignerResultButton.grid(column=1, row=self.currentRow, sticky='w')
        self.layoutEndRow(colorFrame, 10)

        bgLocalNameVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(bgLocalName=bgLocalNameVariable.get()))
        colorLocalNameVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(colorLocalName=colorLocalNameVariable.get()))
        bgLocalResultVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(bgLocalResult=bgLocalResultVariable.get()))
        colorLocalResultVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            colorLocalResult=colorLocalResultVariable.get()))
        bgForeignerNameVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(bgForeignerName=bgForeignerNameVariable.get()))
        colorForeignerNameVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            colorForeignerName=colorForeignerNameVariable.get()))
        bgForeignerResultVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            bgForeignerResult=bgForeignerResultVariable.get()))
        colorForeignerResultVariable.trace_add('write', lambda var, index, mode: self.updateExampleLines(
            colorForeignerResult=colorForeignerResultVariable.get()))

        # Animation

        animationFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(animationFrame, text='Animation')
        animationFrame.columnconfigure(0, weight=1)
        animationFrame.columnconfigure(1, weight=1)
        self.currentRow = 0
        emptyFrames = []

        animationLabel = tk.Label(colorFrame, text='Customize the animation parameters')
        animationLabel.grid(column=0, columnspan=2, row=self.currentRow)

        self.layoutEndRow(animationFrame, 10)
        emptyFrames.append(tk.Frame(animationFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(animationFrame, 30)

        durationXLabel = tk.Label(animationFrame, text='Duration of expansion/reduction of a focused line (in milliseconds)')
        durationXLabel.grid(column=0, row=self.currentRow, sticky='e')
        durationXVariable = tk.StringVar()
        durationXSpinbox = tk.Spinbox(animationFrame, width=20, from_=0, to=10000, textvariable=durationXVariable)
        durationXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        durationXVariable.set(f'{self.durationX}')
        self.layoutEndRow(animationFrame, 10)

        FPSXLabel = tk.Label(animationFrame, text='FPS for expansion/reduction of a focused line')
        FPSXLabel.grid(column=0, row=self.currentRow, sticky='e')
        FPSXVariable = tk.StringVar()
        FPSXSpinbox = tk.Spinbox(animationFrame, width=20, from_=0, to=100, textvariable=FPSXVariable)
        FPSXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        FPSXVariable.set(f'{self.FPSX}')

        self.layoutEndRow(animationFrame, 10)
        emptyFrames.append(tk.Frame(animationFrame))
        emptyFrames[-1].grid(column=0, columnspan=2, row=self.currentRow)
        self.layoutEndRow(animationFrame, 30)

        durationYLabel = tk.Label(animationFrame, text='Duration of ranking update')
        durationYLabel.grid(column=0, row=self.currentRow, sticky='e')
        durationYVariable = tk.StringVar()
        durationYSpinbox = tk.Spinbox(animationFrame, width=20, from_=0, to=10000, textvariable=durationYVariable)
        durationYSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        durationYVariable.set(f'{self.durationY}')
        self.layoutEndRow(animationFrame, 10)

        FPSYLabel = tk.Label(animationFrame, text='FPS for ranking update')
        FPSYLabel.grid(column=0, row=self.currentRow, sticky='e')
        FPSYVariable = tk.StringVar()
        FPSYSpinbox = tk.Spinbox(animationFrame, width=20, from_=0, to=100, textvariable=FPSYVariable)
        FPSYSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        FPSYVariable.set(f'{self.FPSY}')

        # End

        OKButton = tk.Button(layoutWindow, text='OK', command=lambda: self.updateLayoutCloseButton(
            cleverInt(widthRankingVariable.get()), cleverInt(widthFlagRectangleVariable.get()), cleverInt(heightFlagVariable.get()), cleverInt(widthNameVariable.get()), cleverInt(widthFullNameVariable.get(
            )), cleverInt(widthCountVariable.get()), cleverInt(widthResultVariable.get()), cleverInt(widthFullResultVariable.get()), cleverInt(heightVariable.get()), cleverInt(heightSeparatorVariable.get()),
            fontFamilyVariable.get(),
            cleverInt(rankingSizeVariable.get()), timeTowerUtils.getModifiers(self.rankingBoldVariable.get(), self.rankingItalicVariable.get()),
            cleverInt(nameSizeVariable.get()), timeTowerUtils.getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()),
            cleverInt(countSizeVariable.get()), timeTowerUtils.getModifiers(self.countBoldVariable.get(), self.countItalicVariable.get()),
            cleverInt(incompleteResultSizeVariable.get()), timeTowerUtils.getModifiers(
                self.incompleteResultBoldVariable.get(), self.incompleteResultItalicVariable.get()),
            cleverInt(resultSizeVariable.get()), timeTowerUtils.getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()),
            cleverInt(fullResultSizeVariable.get()), timeTowerUtils.getModifiers(
                self.fullResultBoldVariable.get(), self.fullResultItalicVariable.get()),
            bgLocalNameVariable.get(), bgLocalResultVariable.get(),
            bgForeignerNameVariable.get(), bgForeignerResultVariable.get(),
            colorLocalNameVariable.get(), colorLocalResultVariable.get(),
            colorForeignerNameVariable.get(), colorForeignerResultVariable.get(),
            cleverInt(durationXVariable.get()), cleverInt(FPSXVariable.get()),
            cleverInt(durationYVariable.get()), cleverInt(FPSYVariable.get()),
            layoutWindow))
        OKButton.pack(pady=30)

        self.createExampleLines(layoutWindow)

    def updateAnimationSettingsCloseButton(self, durationX, FPSX, durationY, FPSY, window):
        try:
            self.durationX = int(durationX)
            self.FPSX = int(FPSX)
            self.durationY = int(durationY)
            self.FPSY = int(FPSY)
        except:
            tkinter.messagebox.showerror(title='Animation Settings Error !', message='All numbers must be integer!')
        else:
            self.loadContent()
            window.destroy()

    def updateTelegramSettingsCloseButton(self, token, id, window):
        self.botToken = token
        self.botChannelId = id
        try:
            if self.bot is None:
                self.bot = TelegramBot.TelegramBot(self.botToken, self.botChannelId, False, True)
                self.bot.sendSimpleMessage('Bot TimeTower ready')
                self.bot.setMessageHandler(['timeTowerEvent'], self.timeTowerEventCallback)
                self.bot.setMessageHandler(['timeTowerExpand'], self.timeTowerExpandCallback)
                self.threadBot = threading.Thread(target=self.bot.startPolling)
                self.threadBot.daemon = True
                self.threadBot.start()
        except:
            tkinter.messagebox.showerror(
                title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct')
        else:
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

    def showSettingsFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black', highlightthickness=1)
        settingsLabel = tk.Label(frame, text='TimeTower Settings', bg=self.BG_COLOR)
        settingsLabel.grid(column=0, row=0)
        compIdButton = tk.Button(frame, text='Update competition ID', command=self.updateCompId)
        compIdButton.grid(column=0, row=1)
        delayButton = tk.Button(frame, text='Update refresh delay', command=self.updateDelay)
        delayButton.grid(column=0, row=2)
        regionButton = tk.Button(frame, text='Update championship region', command=self.updateRegion)
        regionButton.grid(column=0, row=3)
        layoutButton = tk.Button(frame, text='Update layout', command=self.updateLayout)
        layoutButton.grid(column=0, row=4)
        telegramButton = tk.Button(frame, text='Change Telegram Settings', command=self.updateTelegramSettings)
        telegramButton.grid(column=0, row=5)
        saveButton = tk.Button(frame, text='Save TimeTower Settings...', command=self.saveSettings)
        saveButton.grid(column=0, row=6)
        saveButton = tk.Button(frame, text='Load TimeTower Settings...', command=self.loadSettings)
        saveButton.grid(column=0, row=7)
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
