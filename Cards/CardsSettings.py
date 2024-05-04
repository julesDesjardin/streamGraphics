import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
import json
import queue
import threading
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import cv2

import constants
import utils
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot, Flag


class CardsSettings:

    BG_COLOR = '#F4ECE1'

    def __init__(self, root, camerasCount):
        self.root = root
        self.mainFrame = tk.Frame(self.root)
        self.camerasCount = camerasCount
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.queues = []
        self.canvases = []
        self.texts = []
        self.flags = []
        self.flagImages = []
        self.backgrounds = []
        self.loopFile = ''
        self.loopImages = []
        self.introFile = ''
        self.introImages = []
        self.width = constants.DEFAULT_WIDTH
        self.height = constants.DEFAULT_HEIGHT
        self.backgroundColor = '#FFFFFF'
        self.font = constants.DEFAULT_FONT
        self.textX = 0
        self.textY = 0
        self.flagX = constants.DEFAULT_FLAG_X
        self.flagY = constants.DEFAULT_FLAG_Y
        self.flagWidth = constants.DEFAULT_FLAG_WIDTH
        self.flagHeight = constants.DEFAULT_FLAG_HEIGHT
        self.exampleFlag = Flag.getFlag(self.flagWidth, self.flagHeight, 'local')
        for i in range(0, camerasCount):
            self.queues.append(queue.Queue())
            self.canvases.append(tkinter.Canvas(self.mainFrame, width=self.width, height=self.height, background=self.backgroundColor))
            self.backgrounds.append(self.canvases[i].create_image(0, 0, anchor='nw'))
            self.texts.append(self.canvases[i].create_text(self.textX, self.textY, font=self.font, text=f'Camera {i+1} text', anchor='nw'))
            self.flags.append(Flag.getFlag(self.flagWidth, self.flagHeight, 'local'))
            self.flagImages.append(self.canvases[i].create_image(self.flagX, self.flagY, image=self.flags[i]))

    def botCallback(self, message):
        fullMessage = message.text.removeprefix('/cardData ')
        camera = int(fullMessage[0])
        if len(fullMessage) > 4:
            country = fullMessage[2:4]
            data = fullMessage[5:]
            self.queues[camera].put((country, data))
        else:
            self.queues[camera].put(('', ''))

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./', filetypes=(("JSON Files", "*.json"),
                                                    ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'width': self.width,
            'height': self.height,
            'backgroundColor': self.backgroundColor,
            'introFile': self.introFile,
            'loopFile': self.loopFile,
            'font': self.font,
            'textX': self.textX,
            'textY': self.textY,
            'flagX': self.flagX,
            'flagY': self.flagY,
            'flagWidth': self.flagWidth,
            'flagHeight': self.flagHeight,
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
            self.width = loadSettingsJson['width']
            self.height = loadSettingsJson['height']
            self.backgroundColor = loadSettingsJson['backgroundColor']
            self.introFile = loadSettingsJson['introFile']
            self.loopFile = loadSettingsJson['loopFile']
            self.font = loadSettingsJson['font']
            self.textX = loadSettingsJson['textX']
            self.textY = loadSettingsJson['textY']
            self.flagX = loadSettingsJson['flagX']
            self.flagY = loadSettingsJson['flagY']
            self.flagWidth = loadSettingsJson['flagWidth']
            self.flagHeight = loadSettingsJson['flagHeight']
            self.botToken = loadSettingsJson['botToken']
            self.botChannelId = loadSettingsJson['botChannelId']
        except:
            tkinter.messagebox.showerror(title='Settings Error !',
                                         message='Error in the Settings file, please make sure you selected the correct file and try to load again')
            return

        try:
            self.flags.clear()
            for i in range(0, self.camerasCount):
                self.canvases[i].configure(width=self.width, height=self.height, background=self.backgroundColor)
                self.canvases[i].coords(self.texts[i], self.textX, self.textY)
                self.flags.append(Flag.getFlag(self.flagWidth, self.flagHeight, 'local'))
                self.canvases[i].itemconfig(self.flagImages[i], image=self.flags[i])
                self.canvases[i].coords(self.flagImages[i], self.flagX, self.flagY)
                if not self.canvases[i].winfo_ismapped():
                    self.canvases[i].pack(side=tk.LEFT, padx=10)
        except:
            tkinter.messagebox.showerror(title='Cards Error !',
                                         message='Error in the Cards Settings, please make sure the Settings are correct')

        if self.loopFile != '':
            utils.loadVideo(self.loopFile, self.loopImages)
            for i in range(0, self.camerasCount):
                self.canvases[i].itemconfig(self.backgrounds[i], image=self.loopImages[0])

        if self.introFile != '':
            utils.loadVideo(self.introFile, self.introImages)

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

    def updateBackgroundCloseButton(self, window, introFile, loopFile, canvas, background, width, height):
        self.introFile = introFile
        if self.introFile != '':
            utils.loadVideo(self.introFile, self.introImages)
        self.loopFile = loopFile
        if self.loopFile != '':
            (widthVideo, heightVideo) = utils.loadVideo(self.loopFile, self.loopImages)
            canvas.configure(width=widthVideo, height=heightVideo)
            width.set(widthVideo)
            height.set(heightVideo)
            canvas.itemconfig(background, image=self.loopImages[0])
        window.destroy()

    def updateBackground(self, window, canvas, background, width, height):
        backgroundWindow = tk.Toplevel(window)
        backgroundWindow.grab_set()

        introLabel = tk.Label(backgroundWindow, text='Intro video/image')
        introLabel.grid(row=0, column=0)
        introEntry = tk.Entry(backgroundWindow)
        introEntry.delete(0, tkinter.END)
        introEntry.insert(0, self.loopFile)
        introEntry.grid(row=0, column=1)
        introBrowse = tk.Button(backgroundWindow, text='Browse...', command=lambda: utils.browse(introEntry))
        introBrowse.grid(row=0, column=2)
        loopLabel = tk.Label(backgroundWindow, text='Background video/image')
        loopLabel.grid(row=1, column=0)
        loopEntry = tk.Entry(backgroundWindow)
        loopEntry.delete(0, tkinter.END)
        loopEntry.insert(0, self.loopFile)
        loopEntry.grid(row=1, column=1)
        loopBrowse = tk.Button(backgroundWindow, text='Browse...', command=lambda: utils.browse(loopEntry))
        loopBrowse.grid(row=1, column=2)

        OKButton = tk.Button(backgroundWindow, text='OK', command=lambda: self.updateBackgroundCloseButton(
            backgroundWindow, introEntry.get(), loopEntry.get(), canvas, background, width, height))
        OKButton.grid(row=2, column=0, columnspan=3)

    def updateLayoutCloseButton(self, window, width, height, textX, textY, flagWidth, flagHeight, flagX, flagY):
        self.width = width
        self.height = height
        self.textX = textX
        self.textY = textY
        self.flagWidth = flagWidth
        self.flagHeight = flagHeight
        self.flagX = flagX
        self.flagY = flagY
        for i in range(0, self.camerasCount):
            self.canvases[i].configure(width=self.width, height=self.height, background=self.backgroundColor)
            self.canvases[i].itemconfig(self.backgrounds[i], image=self.loopImages[0])
            self.canvases[i].coords(self.texts[i], self.textX, self.textY)
            self.flags[i] = Flag.getFlag(self.flagWidth, self.flagHeight, 'local')
            self.canvases[i].itemconfig(self.flagImages[i], image=self.flags[i])
            self.canvases[i].coords(self.flagImages[i], self.flagX, self.flagY)
            if not self.canvases[i].winfo_ismapped():
                self.canvases[i].pack(side=tk.LEFT, padx=10)

        window.destroy()

    def updateFlag(self, canvas, flag, flagWidth, flagHeight):
        self.exampleFlag = Flag.getFlag(flagWidth, flagHeight, 'local')
        canvas.itemconfig(flag, image=self.exampleFlag)

    def updateLayout(self):
        layoutWindow = tk.Toplevel(self.root)
        layoutWindow.grab_set()
        layoutWindow.rowconfigure(0, pad=10)
        layoutWindow.rowconfigure(1, pad=10)
        layoutWindow.rowconfigure(2, pad=10)
        layoutWindow.rowconfigure(3, pad=10)
        layoutWindow.rowconfigure(4, pad=10)
        layoutLabel = tk.Label(layoutWindow, text='Customize the cards layout')
        layoutLabel.grid(column=0, row=0, columnspan=4)

        widthLabel = tk.Label(layoutWindow, text='Card width')
        widthLabel.grid(column=0, row=1, sticky='e')
        widthVariable = tk.StringVar()
        widthSpinbox = tk.Spinbox(layoutWindow, width=20, from_=0, to=2000, textvariable=widthVariable)
        widthSpinbox.grid(column=1, row=1, sticky='w')
        widthVariable.set(f'{self.width}')

        heightLabel = tk.Label(layoutWindow, text='Card height')
        heightLabel.grid(column=2, row=1, sticky='e')
        heightVariable = tk.StringVar()
        heightSpinbox = tk.Spinbox(layoutWindow, width=20, from_=0, to=2000, textvariable=heightVariable)
        heightSpinbox.grid(column=3, row=1, sticky='w')
        heightVariable.set(f'{self.height}')

        textXLabel = tk.Label(layoutWindow, text='Text position X')
        textXLabel.grid(column=0, row=2, sticky='e')
        textXVariable = tk.StringVar()
        textXSpinbox = tk.Spinbox(layoutWindow, from_=0, to=self.width, textvariable=textXVariable)
        textXSpinbox.grid(column=1, row=2, sticky='w')
        textXVariable.set(f'{self.textX}')

        textYLabel = tk.Label(layoutWindow, text='Text position Y')
        textYLabel.grid(column=2, row=2, sticky='e')
        textYVariable = tk.StringVar()
        textYSpinbox = tk.Spinbox(layoutWindow, from_=0, to=self.height, textvariable=textYVariable)
        textYSpinbox.grid(column=3, row=2, sticky='w')
        textYVariable.set(f'{self.textY}')

        flagWidthLabel = tk.Label(layoutWindow, text='Flag width')
        flagWidthLabel.grid(column=0, row=3, sticky='e')
        flagWidthVariable = tk.StringVar()
        flagWidthSpinbox = tk.Spinbox(layoutWindow, width=20, from_=0, to=2000, textvariable=flagWidthVariable)
        flagWidthSpinbox.grid(column=1, row=3, sticky='w')
        flagWidthVariable.set(f'{self.flagWidth}')

        flagHeightLabel = tk.Label(layoutWindow, text='Flag height')
        flagHeightLabel.grid(column=2, row=3, sticky='e')
        flagHeightVariable = tk.StringVar()
        flagHeightSpinbox = tk.Spinbox(layoutWindow, width=20, from_=0, to=2000, textvariable=flagHeightVariable)
        flagHeightSpinbox.grid(column=3, row=3, sticky='w')
        flagHeightVariable.set(f'{self.flagHeight}')

        flagXLabel = tk.Label(layoutWindow, text='Flag position X')
        flagXLabel.grid(column=0, row=4, sticky='e')
        flagXVariable = tk.StringVar()
        flagXSpinbox = tk.Spinbox(layoutWindow, from_=0, to=self.width, textvariable=flagXVariable)
        flagXSpinbox.grid(column=1, row=4, sticky='w')
        flagXVariable.set(f'{self.flagX}')

        flagYLabel = tk.Label(layoutWindow, text='Flag position Y')
        flagYLabel.grid(column=2, row=4, sticky='e')
        flagYVariable = tk.StringVar()
        flagYSpinbox = tk.Spinbox(layoutWindow, from_=0, to=self.height, textvariable=flagYVariable)
        flagYSpinbox.grid(column=3, row=4, sticky='w')
        flagYVariable.set(f'{self.flagY}')

        backgroundButton = tk.Button(layoutWindow, text='Update background image/video',
                                     command=lambda: self.updateBackground(layoutWindow, exampleCanvas, exampleBackground, widthVariable, heightVariable))
        backgroundButton.grid(column=0, row=5, columnspan=4)

        OKButton = tk.Button(layoutWindow, text='OK', command=lambda: self.updateLayoutCloseButton(
            layoutWindow, int(widthVariable.get()), int(heightVariable.get()), int(textXVariable.get()), int(textYVariable.get()), int(flagWidthVariable.get()), int(flagHeightVariable.get()), int(flagXVariable.get()), int(flagYVariable.get())))
        OKButton.grid(column=0, row=6, columnspan=4)

        # TODO Background color
        # TODO Font ?

        exampleCanvas = tk.Canvas(layoutWindow, width=self.width, height=self.height, background=self.backgroundColor)
        exampleCanvas.grid(column=0, row=7, columnspan=4)
        exampleBackground = exampleCanvas.create_image(0, 0, anchor='nw')
        exampleText = exampleCanvas.create_text(self.textX, self.textY, font=self.font, text=f'Lorem ipsum', anchor='nw')
        self.exampleFlag = Flag.getFlag(self.flagWidth, self.flagHeight, 'local')
        exampleFlagImage = exampleCanvas.create_image(self.flagX, self.flagY, image=self.exampleFlag)

        widthVariable.trace_add('write', lambda var, index, mode: exampleCanvas.configure(width=int(widthVariable.get())))
        heightVariable.trace_add('write', lambda var, index, mode: exampleCanvas.configure(height=int(heightVariable.get())))
        textXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleText, int(textXVariable.get()), int(textYVariable.get())))
        textYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleText, int(textXVariable.get()), int(textYVariable.get())))
        flagWidthVariable.trace_add('write', lambda var, index, mode: self.updateFlag(
            exampleCanvas, exampleFlagImage, int(flagWidthVariable.get()), int(flagHeightVariable.get())))
        flagHeightVariable.trace_add('write', lambda var, index, mode: self.updateFlag(
            exampleCanvas, exampleFlagImage, int(flagWidthVariable.get()), int(flagHeightVariable.get())))
        flagXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleFlagImage, int(flagXVariable.get()), int(flagYVariable.get())))
        flagYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleFlagImage, int(flagXVariable.get()), int(flagYVariable.get())))

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
        layoutButton = tk.Button(frame, text='Update layout', command=self.updateLayout)
        layoutButton.grid(column=0, row=1)
        telegramButton = tk.Button(frame, text='Change Telegram Settings', command=self.updateTelegramSettings)
        telegramButton.grid(column=0, row=2)
        saveButton = tk.Button(frame, text='Save Settings...', command=self.saveSettings)
        saveButton.grid(column=0, row=3)
        saveButton = tk.Button(frame, text='Load Settings...', command=self.loadSettings)
        saveButton.grid(column=0, row=4)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
        frame.rowconfigure(4, pad=20)
