import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk, font
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
                                  self.height, self.heightSeparator, self.maxNumber, self.delay, stepXmax, stepYmax, durationX, durationY))

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
            self.exampleLines[0].bgName = bgForeignerName
        if bgForeignerResult is not None:
            self.exampleLines[0].bgResult = bgForeignerResult
        if colorLocalName is not None:
            self.exampleLines[0].colorName = colorLocalName
        if colorLocalResult is not None:
            self.exampleLines[0].colorResult = colorLocalResult
        if colorForeignerName is not None:
            self.exampleLines[0].colorName = colorForeignerName
        if colorForeignerResult is not None:
            self.exampleLines[0].colorResult = colorForeignerResult

        self.exampleCanvas.delete('all')
        for line in self.exampleLines:
            line.showLine(0, 0)

    def updateLayoutCloseButton(self, widthRanking, widthFlagRectangle, heightFlag, widthName, widthFullName, widthCount, widthResult, widthFullResult, height, heightSeparator, window):
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
        except:
            tkinter.messagebox.showerror(title='Layout Settings Error !', message='Error in the settings! Please check all values.')
        else:
            self.loadContent()
            window.destroy()

    def updateLayout(self):
        layoutWindow = tk.Toplevel(self.root)
        layoutWindow.grab_set()

        layoutLabel = tk.Label(layoutWindow, text='Customize the tower layout')
        layoutLabel.pack(pady=5)

        layoutNotebook = ttk.Notebook(layoutWindow)
        layoutNotebook.pack(pady=5)

        # Size

        sizeFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(sizeFrame, text='Size')
        self.currentRow = 0
        emptyFrames = []

        self.layoutEndRow(sizeFrame, 10)
        emptyFrames.append(tk.Frame(sizeFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(sizeFrame, 30)

        widthRankingLabel = tk.Label(sizeFrame, text='Ranking width:')
        widthRankingLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthRankingVariable = tk.StringVar()
        widthRankingSpinbox = tk.Spinbox(sizeFrame, from_=0, to=timeTowerUtils.LAYOUT_MAX_WIDTH, textvariable=widthRankingVariable)
        widthRankingSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthRankingVariable.set(f'{self.widthRanking}')

        self.layoutEndRow(sizeFrame, 10)
        emptyFrames.append(tk.Frame(sizeFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
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
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
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
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
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
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
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

        # End

        OKButton = tk.Button(layoutWindow, text='OK', command=lambda: self.updateLayoutCloseButton(
            cleverInt(widthRankingVariable.get()), cleverInt(widthFlagRectangleVariable.get()), cleverInt(heightFlagVariable.get()), cleverInt(widthNameVariable.get()), cleverInt(widthFullNameVariable.get()), cleverInt(widthCountVariable.get()), cleverInt(widthResultVariable.get()), cleverInt(widthFullResultVariable.get()), cleverInt(heightVariable.get()), cleverInt(heightSeparatorVariable.get()), layoutWindow))
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

    def updateAnimationSettings(self):
        animationWindow = tk.Toplevel(self.root)
        animationWindow.grab_set()
        animationWindow.columnconfigure(0, pad=10)
        animationWindow.columnconfigure(1, pad=10)
        animationWindow.rowconfigure(0, pad=10)
        animationWindow.rowconfigure(1, pad=10)
        animationWindow.rowconfigure(2, pad=10)
        animationWindow.rowconfigure(3, pad=10)
        animationWindow.rowconfigure(4, pad=10)
        animationWindow.rowconfigure(5, pad=50)
        animationLabel = tk.Label(animationWindow, text='Update animation settings for expanding lines and updating results')
        animationLabel.grid(row=0, column=0, columnspan=2)
        durationXLabel = tk.Label(animationWindow, text='Duration of expansion/reduction of a focused line (in milliseconds)')
        durationXLabel.grid(row=1, column=0, sticky='e')
        durationXVariable = tk.StringVar()
        durationXSpinbox = tk.Spinbox(animationWindow, width=20, from_=0, to=10000, textvariable=durationXVariable)
        durationXSpinbox.grid(row=1, column=1, sticky='w')
        durationXVariable.set(f'{self.durationX}')
        FPSXLabel = tk.Label(animationWindow, text='FPS for expansion/reduction of a focused line')
        FPSXLabel.grid(row=2, column=0, sticky='e')
        FPSXVariable = tk.StringVar()
        FPSXSpinbox = tk.Spinbox(animationWindow, width=20, from_=0, to=100, textvariable=FPSXVariable)
        FPSXSpinbox.grid(row=2, column=1, sticky='w')
        FPSXVariable.set(f'{self.FPSX}')
        durationYLabel = tk.Label(animationWindow, text='Duration of ranking update')
        durationYLabel.grid(row=3, column=0, sticky='e')
        durationYVariable = tk.StringVar()
        durationYSpinbox = tk.Spinbox(animationWindow, width=20, from_=0, to=10000, textvariable=durationYVariable)
        durationYSpinbox.grid(row=3, column=1, sticky='w')
        durationYVariable.set(f'{self.durationY}')
        FPSYLabel = tk.Label(animationWindow, text='FPS for ranking update')
        FPSYLabel.grid(row=4, column=0, sticky='e')
        FPSYVariable = tk.StringVar()
        FPSYSpinbox = tk.Spinbox(animationWindow, width=20, from_=0, to=100, textvariable=FPSYVariable)
        FPSYSpinbox.grid(row=4, column=1, sticky='w')
        FPSYVariable.set(f'{self.FPSY}')

        OKButton = tk.Button(animationWindow, text='OK', command=lambda: self.updateAnimationSettingsCloseButton(
            durationXVariable.get(), FPSXVariable.get(), durationYVariable.get(), FPSYVariable.get(), animationWindow))
        OKButton.grid(row=5, column=0, columnspan=2)

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
        animationButton = tk.Button(frame, text='Update animation Settings', command=self.updateAnimationSettings)
        animationButton.grid(column=0, row=5)
        telegramButton = tk.Button(frame, text='Change Telegram Settings', command=self.updateTelegramSettings)
        telegramButton.grid(column=0, row=6)
        saveButton = tk.Button(frame, text='Save TimeTower Settings...', command=self.saveSettings)
        saveButton.grid(column=0, row=7)
        saveButton = tk.Button(frame, text='Load TimeTower Settings...', command=self.loadSettings)
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
