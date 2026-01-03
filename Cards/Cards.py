from Common.commonUtils import cleverInt, setModifiersVariables, getModifiers, setAnchorVariables, getAnchor, getJustify, addCheckSettingsChanged, colorButtonCommand, CURRENT_VERSION
from Common import TelegramBot, Image
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk, font
import json
import queue
import threading
import time
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import cv2

import cardsUtils
import DragManager
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')


class Cards:

    BG_COLOR = '#F4ECE1'

    def __init__(self, root):
        self.root = root
        self.mainFrame = tk.Frame(self.root)
        self.botToken = ''
        self.botChannelId = ''
        self.bot = None
        self.loopFile = ''
        self.loopImages = []
        self.introFile = ''
        self.introImages = []
        self.outroFile = ''
        self.outroImages = []
        self.FPS = cardsUtils.DEFAULT_FPS
        self.width = cardsUtils.DEFAULT_WIDTH
        self.height = cardsUtils.DEFAULT_HEIGHT
        self.backgroundColor = '#FFFFFF'
        self.exampleBackgroundImage = None
        self.nameFont = cardsUtils.DEFAULT_FONT_FAMILY
        self.nameSize = cardsUtils.DEFAULT_FONT_SIZE
        self.nameColor = cardsUtils.DEFAULT_FONT_COLOR
        self.nameModifiers = ''
        self.nameAnchor = 'nw'
        self.nameX = 0
        self.nameY = 0
        self.textFont = cardsUtils.DEFAULT_FONT_FAMILY
        self.textSize = cardsUtils.DEFAULT_FONT_SIZE
        self.textColor = cardsUtils.DEFAULT_FONT_COLOR
        self.textModifiers = ''
        self.textAnchor = 'nw'
        self.textX = 0
        self.textY = 0
        self.resultFont = cardsUtils.DEFAULT_FONT_FAMILY
        self.resultSize = cardsUtils.DEFAULT_FONT_SIZE
        self.resultColor = cardsUtils.DEFAULT_FONT_COLOR
        self.resultModifiers = ''
        self.resultAnchor = 'nw'
        self.resultX = 0
        self.resultY = 0
        self.flagEnable = True
        self.flagX = cardsUtils.DEFAULT_FLAG_X
        self.flagY = cardsUtils.DEFAULT_FLAG_Y
        self.flagHeight = cardsUtils.DEFAULT_FLAG_HEIGHT
        self.exampleFlag = Image.getFlag(self.flagHeight, 'local')
        self.avatarEnable = True
        self.avatarX = cardsUtils.DEFAULT_AVATAR_X
        self.avatarY = cardsUtils.DEFAULT_AVATAR_Y
        self.avatarWidth = cardsUtils.DEFAULT_AVATAR_WIDTH
        self.avatarHeight = cardsUtils.DEFAULT_AVATAR_HEIGHT
        self.exampleFlag = Image.getFlag(self.flagHeight, 'local')
        self.exampleAvatar = Image.getAvatar(self.avatarWidth, self.avatarHeight, 'local')
        self.settingsChanged = tk.BooleanVar()
        self.settingsChanged.set(False)
        addCheckSettingsChanged(self.root, self.settingsChanged, self.saveSettings, 'Cards')

        self.showSettingsFrame()
        self.mainFrame.pack(side=tk.RIGHT)
        self.askForReload(cardsUtils.CAMERAS_COLS, cardsUtils.CAMERAS_ROWS)
        self.checkAllQueues()

    def askForReload(self, cols, rows):
        self.reloadCards = (True, cols, rows)

    def cardsInit(self, cols, rows):

        self.cameraCols = cols
        self.cameraRows = rows
        self.camerasCount = self.cameraCols * self.cameraRows
        self.dataQueues = []
        self.resultQueues = []
        self.canvases = []
        self.names = []
        self.texts = []
        self.results = []
        self.flags = []
        self.flagImages = []
        self.avatars = []
        self.avatarImages = []
        self.backgrounds = []
        self.backgroundStates = []
        self.backgroundIndices = []
        self.requestCountries = []
        self.requestNames = []
        self.requestAvatars = []
        self.requestTexts = []
        self.requestResults = []
        for i in range(0, self.camerasCount):
            self.dataQueues.append(queue.Queue())
            self.resultQueues.append(queue.Queue())
            self.canvases.append(tkinter.Canvas(self.mainFrame, width=self.width, height=self.height, background=self.backgroundColor))
            self.backgrounds.append(self.canvases[i].create_image(0, 0, anchor='nw'))
            self.backgroundStates.append(cardsUtils.BackgroundState.EMPTY)
            self.backgroundIndices.append(-1)
            self.requestNames.append('')
            self.requestCountries.append('')
            self.requestAvatars.append('')
            self.requestTexts.append('')
            self.requestResults.append('')
            self.names.append(self.canvases[i].create_text(self.nameX, self.nameY,
                              font=(self.nameFont, self.nameSize, self.nameModifiers), anchor=self.nameAnchor, justify=getJustify(self.nameAnchor)))
            self.texts.append(self.canvases[i].create_text(self.textX, self.textY,
                              font=(self.textFont, self.textSize, self.textModifiers), anchor=self.textAnchor, justify=getJustify(self.textAnchor)))
            self.results.append(self.canvases[i].create_text(self.resultX, self.resultY,
                                font=(self.resultFont, self.resultSize, self.resultModifiers), anchor=self.resultAnchor, justify=getJustify(self.resultAnchor)))
            self.flags.append(Image.getFlag(self.flagHeight, 'local'))
            self.flagImages.append(self.canvases[i].create_image(self.flagX, self.flagY, image=self.flags[i]))
            self.avatars.append(Image.getAvatar(self.avatarWidth, self.avatarHeight, 'local'))
            self.avatarImages.append(self.canvases[i].create_image(self.avatarX, self.avatarY, image=self.avatars[i]))
            self.hide(i)
        for cameraX in range(0, self.cameraCols):
            self.mainFrame.columnconfigure(cameraX, pad=20)
        for cameraY in range(0, self.cameraRows):
            self.mainFrame.rowconfigure(cameraY, pad=20)

        for cameraY in range(0, self.cameraRows):
            for cameraX in range(0, self.cameraCols):
                i = self.cameraCols * cameraY + cameraX
                self.canvases[i].configure(width=self.width, height=self.height, background=self.backgroundColor)
                if self.loopFile != '':
                    self.canvases[i].itemconfig(self.backgrounds[i], image=self.loopImages[0])
                self.canvases[i].itemconfig(self.names[i], font=(self.nameFont, self.nameSize, self.nameModifiers), fill=self.nameColor,
                                            anchor=self.nameAnchor, justify=getJustify(self.nameAnchor))
                self.canvases[i].coords(self.names[i], self.nameX, self.nameY)
                self.canvases[i].itemconfig(self.texts[i], font=(self.textFont, self.textSize, self.textModifiers), fill=self.textColor,
                                            anchor=self.textAnchor, justify=getJustify(self.textAnchor))
                self.canvases[i].coords(self.texts[i], self.textX, self.textY)
                self.flags[i] = Image.getFlag(self.flagHeight, 'local')
                self.canvases[i].itemconfig(self.flagImages[i], image=self.flags[i])
                self.canvases[i].coords(self.flagImages[i], self.flagX, self.flagY)
                if self.flagEnable:
                    self.canvases[i].itemconfig(self.flagImages[i], state='normal')
                else:
                    self.canvases[i].itemconfig(self.flagImages[i], state='hidden')
                self.avatars[i] = Image.getAvatar(self.avatarWidth, self.avatarHeight, 'local')
                self.canvases[i].itemconfig(self.avatarImages[i], image=self.avatars[i])
                self.canvases[i].coords(self.avatarImages[i], self.avatarX, self.avatarY)
                if self.avatarEnable:
                    self.canvases[i].itemconfig(self.avatarImages[i], state='normal')
                else:
                    self.canvases[i].itemconfig(self.avatarImages[i], state='hidden')
                if not self.canvases[i].winfo_ismapped():
                    self.canvases[i].grid(row=cameraY, column=cameraX)
                self.hide(i)

    def dataCallback(self, message):
        messageArray = message.split(TelegramBot.DATA_SPLIT_SYMBOL)
        camera = int(messageArray[0])
        country = messageArray[1]
        name = messageArray[2]
        avatar = messageArray[3]
        if len(messageArray) > 4:
            data = messageArray[4]
        else:
            data = ''
        self.dataQueues[camera].put((country, name, avatar, data))

    def resultCallback(self, message):
        messageArray = message.split(TelegramBot.DATA_SPLIT_SYMBOL)
        camera = int(messageArray[0])
        result = messageArray[1]
        self.resultQueues[camera].put(result)

    def saveSettings(self):
        saveFile = tkinter.filedialog.asksaveasfile(initialdir='./', filetypes=(("JSON Files", "*.json"),
                                                    ("All Files", "*.*")), defaultextension='.json')
        saveSettingsJson = {
            'version': CURRENT_VERSION,
            'cameraRows': self.cameraRows,
            'cameraCols': self.cameraCols,
            'width': self.width,
            'height': self.height,
            'backgroundColor': self.backgroundColor,
            'introFile': self.introFile,
            'outroFile': self.outroFile,
            'loopFile': self.loopFile,
            'FPS': self.FPS,
            'nameFont': self.nameFont,
            'nameSize': self.nameSize,
            'nameColor': self.nameColor,
            'nameModifiers': self.nameModifiers,
            'nameAnchor': self.nameAnchor,
            'nameX': self.nameX,
            'nameY': self.nameY,
            'textFont': self.textFont,
            'textSize': self.textSize,
            'textColor': self.textColor,
            'textModifiers': self.textModifiers,
            'textAnchor': self.textAnchor,
            'textX': self.textX,
            'textY': self.textY,
            'resultFont': self.resultFont,
            'resultSize': self.resultSize,
            'resultColor': self.resultColor,
            'resultModifiers': self.resultModifiers,
            'resultAnchor': self.resultAnchor,
            'resultX': self.resultX,
            'resultY': self.resultY,
            'flagEnable': self.flagEnable,
            'flagX': self.flagX,
            'flagY': self.flagY,
            'flagHeight': self.flagHeight,
            'avatarEnable': self.avatarEnable,
            'avatarX': self.avatarX,
            'avatarY': self.avatarY,
            'avatarWidth': self.avatarWidth,
            'avatarHeight': self.avatarHeight,
            'botToken': self.botToken,
            'botChannelId': self.botChannelId
        }
        saveFile.write(json.dumps(saveSettingsJson, indent=4))
        self.settingsChanged.set(False)

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
            if 'version' not in loadSettingsJson:
                loadSettingsJson['version'] = 10
            # Retrocompat
            version = loadSettingsJson['version']
            if version < 20:
                loadSettingsJson['cameraCols'] = cardsUtils.CAMERAS_COLS
                loadSettingsJson['cameraRows'] = cardsUtils.CAMERAS_ROWS
                loadSettingsJson['resultFont'] = cardsUtils.DEFAULT_FONT_FAMILY
                loadSettingsJson['resultSize'] = cardsUtils.DEFAULT_FONT_SIZE
                loadSettingsJson['resultColor'] = cardsUtils.DEFAULT_FONT_COLOR
                loadSettingsJson['resultModifiers'] = ''
                loadSettingsJson['resultAnchor'] = 'nw'
                loadSettingsJson['resultX'] = 0
                loadSettingsJson['resultY'] = 0
            rows = loadSettingsJson['cameraRows']
            cols = loadSettingsJson['cameraCols']
            self.width = loadSettingsJson['width']
            self.height = loadSettingsJson['height']
            self.backgroundColor = loadSettingsJson['backgroundColor']
            self.introFile = loadSettingsJson['introFile']
            self.outroFile = loadSettingsJson['outroFile']
            self.loopFile = loadSettingsJson['loopFile']
            self.FPS = loadSettingsJson['FPS']
            self.nameFont = loadSettingsJson['nameFont']
            self.nameSize = loadSettingsJson['nameSize']
            self.nameColor = loadSettingsJson['nameColor']
            self.nameModifiers = loadSettingsJson['nameModifiers']
            self.nameAnchor = loadSettingsJson['nameAnchor']
            self.nameX = loadSettingsJson['nameX']
            self.nameY = loadSettingsJson['nameY']
            self.textFont = loadSettingsJson['textFont']
            self.textSize = loadSettingsJson['textSize']
            self.textColor = loadSettingsJson['textColor']
            self.textModifiers = loadSettingsJson['textModifiers']
            self.textAnchor = loadSettingsJson['textAnchor']
            self.textX = loadSettingsJson['textX']
            self.textY = loadSettingsJson['textY']
            self.resultFont = loadSettingsJson['resultFont']
            self.resultSize = loadSettingsJson['resultSize']
            self.resultColor = loadSettingsJson['resultColor']
            self.resultModifiers = loadSettingsJson['resultModifiers']
            self.resultAnchor = loadSettingsJson['resultAnchor']
            self.resultX = loadSettingsJson['resultX']
            self.resultY = loadSettingsJson['resultY']
            self.flagEnable = loadSettingsJson['flagEnable']
            self.flagX = loadSettingsJson['flagX']
            self.flagY = loadSettingsJson['flagY']
            self.flagHeight = loadSettingsJson['flagHeight']
            self.avatarEnable = loadSettingsJson['avatarEnable']
            self.avatarX = loadSettingsJson['avatarX']
            self.avatarY = loadSettingsJson['avatarY']
            self.avatarWidth = loadSettingsJson['avatarWidth']
            self.avatarHeight = loadSettingsJson['avatarHeight']
            self.botToken = loadSettingsJson['botToken']
            self.botChannelId = loadSettingsJson['botChannelId']
        except:
            tkinter.messagebox.showerror(title='Settings Error !',
                                         message='Error in the Settings file, please make sure you selected the correct file and try to load again')
            return

        self.askForReload(cols, rows)

        if self.loopFile != '':
            cardsUtils.loadVideo(self.loopFile, self.loopImages)

        if self.introFile != '':
            cardsUtils.loadVideo(self.introFile, self.introImages)

        if self.outroFile != '':
            cardsUtils.loadVideo(self.outroFile, self.outroImages)

        try:
            if self.bot is None:
                self.bot = TelegramBot.TelegramBot(self.botToken, self.botChannelId, False, True)
                self.bot.sendSimpleMessage('Bot Cards ready')
                self.bot.setMessageHandler(['cardData'], self.dataCallback)
                self.bot.setMessageHandler(['cardResult'], self.resultCallback)
                self.threadBot = threading.Thread(target=self.bot.startPolling)
                self.threadBot.daemon = True
                self.threadBot.start()
        except:
            tkinter.messagebox.showerror(
                title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct, and the application isn\'t already running')
            return
        self.checkAllQueues()
        self.currentlyChanging = False
        self.settingsChanged.set(False)

    def updateCamerasCloseButton(self, cameraRows, cameraCols, window):
        try:
            self.askForReload(int(cameraCols), int(cameraRows))
        except:
            tkinter.messagebox.showerror(title='Cameras Error !', message='Error ! Please make sure both values are numbers')
        else:
            window.destroy()
            self.settingsChanged.set(True)

    def updateCameras(self):
        camerasWindow = tk.Toplevel(self.root)
        camerasWindow.grab_set()
        camerasWindow.rowconfigure(0, pad=20)
        camerasWindow.rowconfigure(1, pad=20)
        camerasWindow.rowconfigure(2, pad=20)
        camerasWindow.rowconfigure(3, pad=20)
        camerasLabel = tk.Label(camerasWindow, text='Please change the number of rows and columns of cameras')
        camerasLabel.grid(column=0, row=0, columnspan=2)
        cameraRowsLabel = tk.Label(camerasWindow, text='Rows:')
        cameraRowsLabel.grid(column=0, row=1, sticky='e')
        cameraRowsVariable = tk.StringVar()
        cameraRowsSpinbox = tk.Spinbox(camerasWindow, from_=1, to=10, textvariable=cameraRowsVariable)
        cameraRowsVariable.set(self.cameraRows)
        cameraRowsSpinbox.grid(column=1, row=1, sticky='w')
        cameraColsLabel = tk.Label(camerasWindow, text='Columns:')
        cameraColsLabel.grid(column=0, row=2, sticky='e')
        cameraColsVariable = tk.StringVar()
        cameraColsSpinbox = tk.Spinbox(camerasWindow, from_=1, to=10, textvariable=cameraColsVariable)
        cameraColsVariable.set(self.cameraCols)
        cameraColsSpinbox.grid(column=1, row=2, sticky='w')
        camerasCloseButton = tk.Button(camerasWindow, text='OK', command=lambda:
                                       self.updateCamerasCloseButton(cameraRowsVariable.get(), cameraColsVariable.get(), camerasWindow))
        camerasCloseButton.grid(column=0, row=3, columnspan=2)

    def updateBackgroundCloseButton(self, window, introFile, loopFile, outroFile, canvas, background, width, height, intro, loop, outro):
        intro.set(introFile)
        loop.set(loopFile)
        outro.set(outroFile)
        if loopFile != '':
            (self.exampleBackgroundImage, widthVideo, heightVideo) = cardsUtils.loadFirstFrame(loopFile)
            canvas.configure(width=widthVideo, height=heightVideo)
            width.set(widthVideo)
            height.set(heightVideo)
            canvas.itemconfig(background, image=self.exampleBackgroundImage)
        window.destroy()
        self.settingsChanged.set(True)

    def updateBackground(self, window, canvas, background, width, height, intro, loop, outro):
        backgroundWindow = tk.Toplevel(window)
        backgroundWindow.grab_set()

        introLabel = tk.Label(backgroundWindow, text='Intro video/image')
        introLabel.grid(row=0, column=0)
        introEntry = tk.Entry(backgroundWindow)
        introEntry.delete(0, tkinter.END)
        introEntry.insert(0, intro.get())
        introEntry.grid(row=0, column=1)
        introBrowse = tk.Button(backgroundWindow, text='Browse...', command=lambda: cardsUtils.browse(introEntry))
        introBrowse.grid(row=0, column=2)
        loopLabel = tk.Label(backgroundWindow, text='Background video/image')
        loopLabel.grid(row=1, column=0)
        loopEntry = tk.Entry(backgroundWindow)
        loopEntry.delete(0, tkinter.END)
        loopEntry.insert(0, loop.get())
        loopEntry.grid(row=1, column=1)
        loopBrowse = tk.Button(backgroundWindow, text='Browse...', command=lambda: cardsUtils.browse(loopEntry))
        loopBrowse.grid(row=1, column=2)
        outroLabel = tk.Label(backgroundWindow, text='Outro video/image')
        outroLabel.grid(row=2, column=0)
        outroEntry = tk.Entry(backgroundWindow)
        outroEntry.delete(0, tkinter.END)
        outroEntry.insert(0, outro.get())
        outroEntry.grid(row=2, column=1)
        outroBrowse = tk.Button(backgroundWindow, text='Browse...', command=lambda: cardsUtils.browse(outroEntry))
        outroBrowse.grid(row=2, column=2)

        OKButton = tk.Button(backgroundWindow, text='OK', command=lambda: self.updateBackgroundCloseButton(
            backgroundWindow, introEntry.get(), loopEntry.get(), outroEntry.get(), canvas, background, width, height, intro, loop, outro))
        OKButton.grid(row=3, column=0, columnspan=3)

    def updateLayoutCloseButton(self, window, backgroundColor, introFile, loopFile, outroFile, width, height, nameFont, nameSize, nameColor, nameAnchor, nameX, nameY, textFont, textSize, textColor, textAnchor, textX, textY, resultFont, resultSize, resultColor, resultAnchor, resultX, resultY, flagEnable, flagHeight, flagX, flagY, avatarEnable, avatarWidth, avatarHeight, avatarX, avatarY):
        self.backgroundColor = backgroundColor
        self.introFile = introFile
        self.loopFile = loopFile
        self.outroFile = outroFile
        if self.introFile != '':
            cardsUtils.loadVideo(self.introFile, self.introImages)
        if self.loopFile != '':
            cardsUtils.loadVideo(self.loopFile, self.loopImages)
        if self.outroFile != '':
            cardsUtils.loadVideo(self.outroFile, self.outroImages)
        self.width = width
        self.height = height
        self.nameFont = nameFont
        self.nameSize = nameSize
        self.nameColor = nameColor
        self.nameAnchor = nameAnchor
        self.nameX = nameX
        self.nameY = nameY
        self.textFont = textFont
        self.textSize = textSize
        self.textColor = textColor
        self.textAnchor = textAnchor
        self.textX = textX
        self.textY = textY
        self.resultFont = resultFont
        self.resultSize = resultSize
        self.resultColor = resultColor
        self.resultAnchor = resultAnchor
        self.resultX = resultX
        self.resultY = resultY
        self.flagEnable = flagEnable
        self.flagHeight = flagHeight
        self.flagX = flagX
        self.flagY = flagY
        self.avatarEnable = avatarEnable
        self.avatarWidth = avatarWidth
        self.avatarHeight = avatarHeight
        self.avatarX = avatarX
        self.avatarY = avatarY

        self.askForReload(self.cameraCols, self.cameraRows)
        window.destroy()
        self.settingsChanged.set(True)

    def enableButtonCallback(self, enable, spinboxes, canvas, images):
        if enable:
            for spinbox in spinboxes:
                spinbox.configure(state='normal')
            for image in images:
                canvas.itemconfig(image, state='normal')
        else:
            for spinbox in spinboxes:
                spinbox.configure(state='disabled')
            for image in images:
                canvas.itemconfig(image, state='hidden')

    def updateFlag(self, canvas, flag, flagHeight):
        self.exampleFlag = Image.getFlag(flagHeight, 'local')
        canvas.itemconfig(flag, image=self.exampleFlag)

    def updateAvatar(self, canvas, avatar, avatarX, avatarY, avatarWidth, avatarHeight, rectangle):
        self.exampleAvatar = Image.getAvatar(avatarWidth, avatarHeight, 'local')
        canvas.itemconfig(avatar, image=self.exampleAvatar)
        canvas.coords(rectangle,
                      avatarX - int(avatarWidth / 2), avatarY - int(avatarHeight / 2), avatarX + int(avatarWidth / 2), avatarY + int(avatarHeight / 2))
        canvas.coords(avatar, avatarX, avatarY)

    def layoutEndRow(self, frame, pad):
        frame.rowconfigure(self.currentRow, pad=pad)
        self.currentRow = self.currentRow + 1

    def updateLayout(self):
        layoutWindow = tk.Toplevel(self.root)
        layoutWindow.grab_set()

        layoutLabel = tk.Label(layoutWindow, text='Customize the Cards:')
        layoutLabel.pack(pady=5)

        layoutNotebook = ttk.Notebook(layoutWindow)
        layoutNotebook.pack(pady=5)

        # Name, text, results

        textFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(textFrame, text='Texts')
        textFrame.columnconfigure(0, weight=1)
        textFrame.columnconfigure(1, weight=1)
        textFrame.columnconfigure(2, weight=1)
        textFrame.columnconfigure(3, weight=1)
        self.currentRow = 0
        emptyFrames = []

        fonts = list(font.families())
        fonts.sort()

        layoutLabel = tk.Label(textFrame, text='Customize the cards layout')
        layoutLabel.grid(column=0, columnspan=4, row=self.currentRow)

        self.layoutEndRow(textFrame, 10)
        emptyFrames.append(tk.Frame(textFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 30)

        widthLabel = tk.Label(textFrame, text='Card width')
        widthLabel.grid(column=0, row=self.currentRow, sticky='e')
        widthVariable = tk.StringVar()
        widthSpinbox = tk.Spinbox(textFrame, width=20, from_=0, to=2000, textvariable=widthVariable)
        widthSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        widthVariable.set(f'{self.width}')

        heightLabel = tk.Label(textFrame, text='Card height')
        heightLabel.grid(column=2, row=self.currentRow, sticky='e')
        heightVariable = tk.StringVar()
        heightSpinbox = tk.Spinbox(textFrame, width=20, from_=0, to=2000, textvariable=heightVariable)
        heightSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        heightVariable.set(f'{self.height}')

        self.layoutEndRow(textFrame, 10)
        emptyFrames.append(tk.Frame(textFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 30)

        nameLabel = tk.Label(textFrame, text='Name:')
        nameLabel.grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 10)

        nameFontLabel = tk.Label(textFrame, text='Name Font')
        nameFontLabel.grid(column=0, row=self.currentRow, sticky='e')
        nameFontVariable = tk.StringVar()
        nameFontMenu = ttk.Combobox(textFrame, textvariable=nameFontVariable)
        nameFontMenu['values'] = fonts
        nameFontVariable.set(self.nameFont)
        nameFontMenu.set(self.nameFont)
        nameFontMenu['state'] = 'readonly'
        nameFontMenu.grid(column=1, row=self.currentRow, sticky='w')

        nameSizeLabel = tk.Label(textFrame, text='Name font size')
        nameSizeLabel.grid(column=2, row=self.currentRow, sticky='e')
        nameSizeVariable = tk.StringVar()
        nameSizeSpinbox = tk.Spinbox(textFrame, from_=0, to=500, textvariable=nameSizeVariable)
        nameSizeSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        nameSizeVariable.set(f'{self.nameSize}')

        self.layoutEndRow(textFrame, 10)

        self.nameBoldVariable = tk.BooleanVar()
        nameBoldCheckbox = tk.Checkbutton(textFrame, text='Bold', variable=self.nameBoldVariable)
        nameBoldCheckbox.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        self.nameItalicVariable = tk.BooleanVar()
        nameItalicCheckbox = tk.Checkbutton(textFrame, text='Italic', variable=self.nameItalicVariable)
        nameItalicCheckbox.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        setModifiersVariables(self.nameModifiers, self.nameBoldVariable, self.nameItalicVariable)

        self.layoutEndRow(textFrame, 10)

        nameColorLabel = tk.Label(textFrame, text='Name color:')
        nameColorLabel.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        nameColorVariable = tk.StringVar()
        nameColorVariable.set(self.nameColor)
        nameColorButtonFrame = tk.Frame(textFrame, highlightbackground='black', highlightthickness=1)
        nameColorButtonFrame.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        nameColorButton = tk.Button(nameColorButtonFrame, text='', background=self.nameColor, relief=tk.FLAT, width=10)
        nameColorButton.configure(command=lambda: colorButtonCommand(nameColorButton, nameColorVariable, 'Name color'))
        nameColorButton.pack()

        self.layoutEndRow(textFrame, 10)

        nameXLabel = tk.Label(textFrame, text='Name position X')
        nameXLabel.grid(column=0, row=self.currentRow, sticky='e')
        nameXVariable = tk.StringVar()
        nameXSpinbox = tk.Spinbox(textFrame, from_=0, to=self.width, textvariable=nameXVariable)
        nameXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        nameXVariable.set(f'{self.nameX}')

        nameYLabel = tk.Label(textFrame, text='Name position Y')
        nameYLabel.grid(column=2, row=self.currentRow, sticky='e')
        nameYVariable = tk.StringVar()
        nameYSpinbox = tk.Spinbox(textFrame, from_=0, to=self.height, textvariable=nameYVariable)
        nameYSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        nameYVariable.set(f'{self.nameY}')

        self.layoutEndRow(textFrame, 10)

        nameAnchorXVariable = tk.StringVar()
        nameAnchorYVariable = tk.StringVar()
        setAnchorVariables(self.nameAnchor, nameAnchorXVariable, nameAnchorYVariable)
        nameAnchorXLabel = tk.Label(textFrame, text='Horizontal alignment')
        nameAnchorXLabel.grid(column=0, row=self.currentRow, sticky='e')
        nameAnchorXMenu = ttk.Combobox(textFrame, textvariable=nameAnchorXVariable, values=['Left', 'Center', 'Right'])
        nameAnchorXMenu.set(nameAnchorXVariable.get())
        nameAnchorXMenu['state'] = 'readonly'
        nameAnchorXMenu.grid(column=1, row=self.currentRow, sticky='w')

        nameAnchorYLabel = tk.Label(textFrame, text='Vertical alignment')
        nameAnchorYLabel.grid(column=2, row=self.currentRow, sticky='e')
        nameAnchorYMenu = ttk.Combobox(textFrame, textvariable=nameAnchorYVariable, values=['Top', 'Center', 'Bottom'])
        nameAnchorYMenu.set(nameAnchorYVariable.get())
        nameAnchorYMenu['state'] = 'readonly'
        nameAnchorYMenu.grid(column=3, row=self.currentRow, sticky='w')

        self.layoutEndRow(textFrame, 10)
        emptyFrames.append(tk.Frame(textFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 30)

        textLabel = tk.Label(textFrame, text='Text:')
        textLabel.grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 10)

        textFontLabel = tk.Label(textFrame, text='Text Font')
        textFontLabel.grid(column=0, row=self.currentRow, sticky='e')
        textFontVariable = tk.StringVar()
        textFontMenu = ttk.Combobox(textFrame, textvariable=textFontVariable)
        textFontMenu['values'] = fonts
        textFontVariable.set(self.textFont)
        textFontMenu.set(self.textFont)
        textFontMenu['state'] = 'readonly'
        textFontMenu.grid(column=1, row=self.currentRow, sticky='w')

        textSizeLabel = tk.Label(textFrame, text='Text font size')
        textSizeLabel.grid(column=2, row=self.currentRow, sticky='e')
        textSizeVariable = tk.StringVar()
        textSizeSpinbox = tk.Spinbox(textFrame, from_=0, to=500, textvariable=textSizeVariable)
        textSizeSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        textSizeVariable.set(f'{self.textSize}')

        self.layoutEndRow(textFrame, 10)

        self.textBoldVariable = tk.BooleanVar()
        textBoldCheckbox = tk.Checkbutton(textFrame, text='Bold', variable=self.textBoldVariable)
        textBoldCheckbox.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        self.textItalicVariable = tk.BooleanVar()
        textItalicCheckbox = tk.Checkbutton(textFrame, text='Italic', variable=self.textItalicVariable)
        textItalicCheckbox.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        setModifiersVariables(self.textModifiers, self.textBoldVariable, self.textItalicVariable)

        self.layoutEndRow(textFrame, 10)

        textColorLabel = tk.Label(textFrame, text='Text color:')
        textColorLabel.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        textColorVariable = tk.StringVar()
        textColorVariable.set(self.textColor)
        textColorButtonFrame = tk.Frame(textFrame, highlightbackground='black', highlightthickness=1)
        textColorButtonFrame.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        textColorButton = tk.Button(textColorButtonFrame, text='', background=self.textColor, relief=tk.FLAT, width=10)
        textColorButton.configure(command=lambda: colorButtonCommand(textColorButton, textColorVariable, 'Text color'))
        textColorButton.pack()

        self.layoutEndRow(textFrame, 10)

        textXLabel = tk.Label(textFrame, text='Text position X')
        textXLabel.grid(column=0, row=self.currentRow, sticky='e')
        textXVariable = tk.StringVar()
        textXSpinbox = tk.Spinbox(textFrame, from_=0, to=self.width, textvariable=textXVariable)
        textXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        textXVariable.set(f'{self.textX}')

        textYLabel = tk.Label(textFrame, text='Text position Y')
        textYLabel.grid(column=2, row=self.currentRow, sticky='e')
        textYVariable = tk.StringVar()
        textYSpinbox = tk.Spinbox(textFrame, from_=0, to=self.height, textvariable=textYVariable)
        textYSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        textYVariable.set(f'{self.textY}')

        self.layoutEndRow(textFrame, 10)

        textAnchorXVariable = tk.StringVar()
        textAnchorYVariable = tk.StringVar()
        setAnchorVariables(self.textAnchor, textAnchorXVariable, textAnchorYVariable)
        textAnchorXLabel = tk.Label(textFrame, text='Horizontal alignment')
        textAnchorXLabel.grid(column=0, row=self.currentRow, sticky='e')
        textAnchorXMenu = ttk.Combobox(textFrame, textvariable=textAnchorXVariable, values=['Left', 'Center', 'Right'])
        textAnchorXMenu.set(textAnchorXVariable.get())
        textAnchorXMenu['state'] = 'readonly'
        textAnchorXMenu.grid(column=1, row=self.currentRow, sticky='w')

        textAnchorYLabel = tk.Label(textFrame, text='Vertical alignment')
        textAnchorYLabel.grid(column=2, row=self.currentRow, sticky='e')
        textAnchorYMenu = ttk.Combobox(textFrame, textvariable=textAnchorYVariable, values=['Top', 'Center', 'Bottom'])
        textAnchorYMenu.set(textAnchorYVariable.get())
        textAnchorYMenu['state'] = 'readonly'
        textAnchorYMenu.grid(column=3, row=self.currentRow, sticky='w')

        self.layoutEndRow(textFrame, 10)
        emptyFrames.append(tk.Frame(textFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 30)

        resultLabel = tk.Label(textFrame, text='Results:')
        resultLabel.grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(textFrame, 10)

        resultFontLabel = tk.Label(textFrame, text='Results Font')
        resultFontLabel.grid(column=0, row=self.currentRow, sticky='e')
        resultFontVariable = tk.StringVar()
        resultFontMenu = ttk.Combobox(textFrame, textvariable=resultFontVariable)
        resultFontMenu['values'] = fonts
        resultFontVariable.set(self.resultFont)
        resultFontMenu.set(self.resultFont)
        resultFontMenu['state'] = 'readonly'
        resultFontMenu.grid(column=1, row=self.currentRow, sticky='w')

        resultSizeLabel = tk.Label(textFrame, text='Results font size')
        resultSizeLabel.grid(column=2, row=self.currentRow, sticky='e')
        resultSizeVariable = tk.StringVar()
        resultSizeSpinbox = tk.Spinbox(textFrame, from_=0, to=500, textvariable=resultSizeVariable)
        resultSizeSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        resultSizeVariable.set(f'{self.resultSize}')

        self.layoutEndRow(textFrame, 10)

        self.resultBoldVariable = tk.BooleanVar()
        resultBoldCheckbox = tk.Checkbutton(textFrame, text='Bold', variable=self.resultBoldVariable)
        resultBoldCheckbox.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        self.resultItalicVariable = tk.BooleanVar()
        resultItalicCheckbox = tk.Checkbutton(textFrame, text='Italic', variable=self.resultItalicVariable)
        resultItalicCheckbox.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        setModifiersVariables(self.resultModifiers, self.resultBoldVariable, self.resultItalicVariable)

        self.layoutEndRow(textFrame, 10)

        resultColorLabel = tk.Label(textFrame, text='Results color:')
        resultColorLabel.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        resultColorVariable = tk.StringVar()
        resultColorVariable.set(self.resultColor)
        resultColorButtonFrame = tk.Frame(textFrame, highlightbackground='black', highlightthickness=1)
        resultColorButtonFrame.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        resultColorButton = tk.Button(resultColorButtonFrame, text='', background=self.resultColor, relief=tk.FLAT, width=10)
        resultColorButton.configure(command=lambda: colorButtonCommand(resultColorButton, resultColorVariable, 'Results color'))
        resultColorButton.pack()

        self.layoutEndRow(textFrame, 10)

        resultXLabel = tk.Label(textFrame, text='Results position X')
        resultXLabel.grid(column=0, row=self.currentRow, sticky='e')
        resultXVariable = tk.StringVar()
        resultXSpinbox = tk.Spinbox(textFrame, from_=0, to=self.width, textvariable=resultXVariable)
        resultXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        resultXVariable.set(f'{self.resultX}')

        resultYLabel = tk.Label(textFrame, text='Results position Y')
        resultYLabel.grid(column=2, row=self.currentRow, sticky='e')
        resultYVariable = tk.StringVar()
        resultYSpinbox = tk.Spinbox(textFrame, from_=0, to=self.height, textvariable=resultYVariable)
        resultYSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        resultYVariable.set(f'{self.resultY}')

        self.layoutEndRow(textFrame, 10)

        resultAnchorXVariable = tk.StringVar()
        resultAnchorYVariable = tk.StringVar()
        setAnchorVariables(self.resultAnchor, resultAnchorXVariable, resultAnchorYVariable)
        resultAnchorXLabel = tk.Label(textFrame, text='Horizontal alignment')
        resultAnchorXLabel.grid(column=0, row=self.currentRow, sticky='e')
        resultAnchorXMenu = ttk.Combobox(textFrame, textvariable=resultAnchorXVariable, values=['Left', 'Center', 'Right'])
        resultAnchorXMenu.set(resultAnchorXVariable.get())
        resultAnchorXMenu['state'] = 'readonly'
        resultAnchorXMenu.grid(column=1, row=self.currentRow, sticky='w')

        resultAnchorYLabel = tk.Label(textFrame, text='Vertical alignment')
        resultAnchorYLabel.grid(column=2, row=self.currentRow, sticky='e')
        resultAnchorYMenu = ttk.Combobox(textFrame, textvariable=resultAnchorYVariable, values=['Top', 'Center', 'Bottom'])
        resultAnchorYMenu.set(resultAnchorYVariable.get())
        resultAnchorYMenu['state'] = 'readonly'
        resultAnchorYMenu.grid(column=3, row=self.currentRow, sticky='w')

        # Images

        imageFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(imageFrame, text='Images')
        imageFrame.columnconfigure(0, weight=1)
        imageFrame.columnconfigure(1, weight=1)
        imageFrame.columnconfigure(2, weight=1)
        imageFrame.columnconfigure(3, weight=1)
        self.currentRow = 0
        emptyFrames = []

        flagEnableVariable = tk.BooleanVar()
        flagEnableVariable.set(self.flagEnable)
        flagEnableButton = tk.Checkbutton(imageFrame, text='Show flag', variable=flagEnableVariable,
                                          command=lambda: self.enableButtonCallback(flagEnableVariable.get(), [flagHeightSpinbox, flagXSpinbox, flagYSpinbox], exampleCanvas, [exampleFlagImage]))
        flagEnableButton.grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(imageFrame, 10)

        flagHeightLabel = tk.Label(imageFrame, text='Flag height')
        flagHeightLabel.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        flagHeightVariable = tk.StringVar()
        flagHeightSpinbox = tk.Spinbox(imageFrame, width=20, from_=0, to=2000, textvariable=flagHeightVariable)
        flagHeightSpinbox.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        flagHeightVariable.set(f'{self.flagHeight}')

        self.layoutEndRow(imageFrame, 10)

        flagXLabel = tk.Label(imageFrame, text='Flag position X')
        flagXLabel.grid(column=0, row=self.currentRow, sticky='e')
        flagXVariable = tk.StringVar()
        flagXSpinbox = tk.Spinbox(imageFrame, from_=0, to=self.width, textvariable=flagXVariable)
        flagXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        flagXVariable.set(f'{self.flagX}')

        flagYLabel = tk.Label(imageFrame, text='Flag position Y')
        flagYLabel.grid(column=2, row=self.currentRow, sticky='e')
        flagYVariable = tk.StringVar()
        flagYSpinbox = tk.Spinbox(imageFrame, from_=0, to=self.height, textvariable=flagYVariable)
        flagYSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        flagYVariable.set(f'{self.flagY}')

        self.layoutEndRow(imageFrame, 10)
        emptyFrames.append(tk.Frame(imageFrame))
        emptyFrames[-1].grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(imageFrame, 30)

        avatarEnableVariable = tk.BooleanVar()
        avatarEnableVariable.set(self.avatarEnable)
        avatarEnableButton = tk.Checkbutton(imageFrame, text='Show avatar', variable=avatarEnableVariable,
                                            command=lambda: self.enableButtonCallback(avatarEnableVariable.get(), [avatarWidthSpinbox, avatarHeightSpinbox, avatarXSpinbox, avatarYSpinbox], exampleCanvas, [exampleAvatarImage, exampleAvatarRectangle]))
        avatarEnableButton.grid(column=0, columnspan=4, row=self.currentRow)
        self.layoutEndRow(imageFrame, 10)

        avatarWidthLabel = tk.Label(imageFrame, text='Avatar Width')
        avatarWidthLabel.grid(column=0, row=self.currentRow, sticky='e')
        avatarWidthVariable = tk.StringVar()
        avatarWidthSpinbox = tk.Spinbox(imageFrame, width=20, from_=0, to=2000, textvariable=avatarWidthVariable)
        avatarWidthSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        avatarWidthVariable.set(f'{self.avatarWidth}')

        avatarHeightLabel = tk.Label(imageFrame, text='Avatar height')
        avatarHeightLabel.grid(column=2, row=self.currentRow, sticky='e')
        avatarHeightVariable = tk.StringVar()
        avatarHeightSpinbox = tk.Spinbox(imageFrame, width=20, from_=0, to=2000, textvariable=avatarHeightVariable)
        avatarHeightSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        avatarHeightVariable.set(f'{self.avatarHeight}')

        self.layoutEndRow(imageFrame, 10)

        avatarXLabel = tk.Label(imageFrame, text='Avatar position X')
        avatarXLabel.grid(column=0, row=self.currentRow, sticky='e')
        avatarXVariable = tk.StringVar()
        avatarXSpinbox = tk.Spinbox(imageFrame, from_=0, to=self.width, textvariable=avatarXVariable)
        avatarXSpinbox.grid(column=1, row=self.currentRow, sticky='w')
        avatarXVariable.set(f'{self.avatarX}')

        avatarYLabel = tk.Label(imageFrame, text='Avatar position Y')
        avatarYLabel.grid(column=2, row=self.currentRow, sticky='e')
        avatarYVariable = tk.StringVar()
        avatarYSpinbox = tk.Spinbox(imageFrame, from_=0, to=self.height, textvariable=avatarYVariable)
        avatarYSpinbox.grid(column=3, row=self.currentRow, sticky='w')
        avatarYVariable.set(f'{self.avatarY}')

        # Background

        backgroundFrame = tk.Frame(layoutNotebook)
        layoutNotebook.add(backgroundFrame, text='Background')
        backgroundFrame.columnconfigure(0, weight=1)
        backgroundFrame.columnconfigure(1, weight=1)
        backgroundFrame.columnconfigure(2, weight=1)
        backgroundFrame.columnconfigure(3, weight=1)
        self.currentRow = 0
        emptyFrames = []

        introFileVariable = tk.StringVar()
        loopFileVariable = tk.StringVar()
        outroFileVariable = tk.StringVar()
        introFileVariable.set(self.introFile)
        loopFileVariable.set(self.loopFile)
        outroFileVariable.set(self.outroFile)
        backgroundButton = tk.Button(backgroundFrame, text='Update background image/video',
                                     command=lambda: self.updateBackground(backgroundFrame, exampleCanvas, exampleBackground, widthVariable, heightVariable, introFileVariable, loopFileVariable, outroFileVariable))
        backgroundButton.grid(column=0, row=self.currentRow, columnspan=4)

        self.layoutEndRow(backgroundFrame, 10)

        backgroundColorLabel = tk.Label(backgroundFrame, text='Background color:')
        backgroundColorLabel.grid(column=0, columnspan=2, row=self.currentRow, sticky='e')
        backgroundColorVariable = tk.StringVar()
        backgroundColorVariable.set(self.backgroundColor)
        backgroundColorButtonFrame = tk.Frame(backgroundFrame, highlightbackground='black', highlightthickness=1)
        backgroundColorButtonFrame.grid(column=2, columnspan=2, row=self.currentRow, sticky='w')
        backgroundColorButton = tk.Button(backgroundColorButtonFrame, text='', background=self.backgroundColor, relief=tk.FLAT, width=10)
        backgroundColorButton.configure(command=lambda: colorButtonCommand(backgroundColorButton, backgroundColorVariable, 'Background color'))
        backgroundColorButton.pack()

        self.layoutEndRow(backgroundFrame, 10)

        OKButton = tk.Button(layoutWindow, text='OK', command=lambda: self.updateLayoutCloseButton(
            layoutWindow, backgroundColorVariable.get(), introFileVariable.get(), loopFileVariable.get(), outroFileVariable.get(),
            int(widthVariable.get()), int(heightVariable.get()),
            nameFontVariable.get(), int(nameSizeVariable.get()), nameColorVariable.get(),
            getAnchor(nameAnchorXVariable.get(), nameAnchorYVariable.get()),
            int(nameXVariable.get()), int(nameYVariable.get()),
            textFontVariable.get(), int(textSizeVariable.get()), textColorVariable.get(),
            getAnchor(textAnchorXVariable.get(), textAnchorYVariable.get()),
            int(textXVariable.get()), int(textYVariable.get()),
            resultFontVariable.get(), int(resultSizeVariable.get()), resultColorVariable.get(),
            getAnchor(resultAnchorXVariable.get(), resultAnchorYVariable.get()),
            int(resultXVariable.get()), int(resultYVariable.get()),
            flagEnableVariable.get(), int(flagHeightVariable.get()), int(flagXVariable.get()), int(flagYVariable.get()),
            avatarEnableVariable.get(), int(avatarWidthVariable.get()), int(avatarHeightVariable.get()), int(avatarXVariable.get()), int(avatarYVariable.get())))
        OKButton.pack(pady=5)

        self.layoutEndRow(backgroundFrame, 10)

        exampleWindow = tk.Toplevel(layoutWindow)
        exampleLabel = tk.Label(
            exampleWindow, text='Example Card. See main window to change sizes, fonts, backgrounds, etc, and confirm changes.\nYou can drag and drop elements (Flag, Avatar, name, extra text) in this window.')
        exampleLabel.pack(pady=20)
        exampleCanvas = tk.Canvas(exampleWindow, width=self.width, height=self.height, background=self.backgroundColor)
        exampleCanvas.pack()
        exampleBackground = exampleCanvas.create_image(0, 0, anchor='nw')
        if self.loopFile != '':
            exampleCanvas.itemconfig(exampleBackground, image=self.loopImages[0])
        self.exampleFlag = Image.getFlag(self.flagHeight, 'local')
        exampleFlagImage = exampleCanvas.create_image(self.flagX, self.flagY, image=self.exampleFlag)
        self.exampleAvatar = Image.getAvatar(self.avatarWidth, self.avatarHeight, 'local')
        exampleAvatarImage = exampleCanvas.create_image(self.avatarX, self.avatarY, image=self.exampleAvatar)
        exampleName = exampleCanvas.create_text(self.nameX, self.nameY, font=(self.nameFont, self.nameSize, self.nameModifiers), fill=self.nameColor,
                                                text=f'Competitor name', anchor=self.nameAnchor, justify=getJustify(self.nameAnchor))
        exampleText = exampleCanvas.create_text(self.textX, self.textY, font=(self.textFont, self.textSize, self.textModifiers), fill=self.textColor,
                                                text=f'Lorem ipsum\nDolor sit amet\nConsectetur adipiscing elit', anchor=self.textAnchor, justify=getJustify(self.textAnchor))
        exampleResult = exampleCanvas.create_text(self.resultX, self.resultY, font=(self.resultFont, self.resultSize, self.resultModifiers), fill=self.resultColor,
                                                  text='1:23.45 (DNF) (1:10.21) 1.51.09', anchor=self.resultAnchor, justify=getJustify(self.resultAnchor))
        exampleAvatarRectangle = exampleCanvas.create_rectangle(
            self.avatarX - int(self.avatarWidth / 2), self.avatarY - int(self.avatarHeight / 2), self.avatarX + int(self.avatarWidth / 2), self.avatarY + int(self.avatarHeight / 2))

        managerFlag = DragManager.DragManager(exampleCanvas, exampleFlagImage, flagXVariable, flagYVariable)
        managerAvatar = DragManager.DragManager(exampleCanvas, exampleAvatarImage, avatarXVariable, avatarYVariable)
        managerName = DragManager.DragManager(exampleCanvas, exampleName, nameXVariable, nameYVariable)
        managerText = DragManager.DragManager(exampleCanvas, exampleText, textXVariable, textYVariable)
        managerResult = DragManager.DragManager(exampleCanvas, exampleResult, resultXVariable, resultYVariable)
        widthVariable.trace_add('write', lambda var, index, mode: exampleCanvas.configure(width=cleverInt(widthVariable.get())))
        widthVariable.trace_add('write', lambda var, index, mode: flagXSpinbox.configure(to=cleverInt(widthVariable.get())))
        widthVariable.trace_add('write', lambda var, index, mode: textXSpinbox.configure(to=cleverInt(widthVariable.get())))
        heightVariable.trace_add('write', lambda var, index, mode: exampleCanvas.configure(height=cleverInt(heightVariable.get())))
        heightVariable.trace_add('write', lambda var, index, mode: flagYSpinbox.configure(to=cleverInt(heightVariable.get())))
        heightVariable.trace_add('write', lambda var, index, mode: textYSpinbox.configure(to=cleverInt(heightVariable.get())))
        nameFontVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleName, font=(nameFontVariable.get(), nameSizeVariable.get(), getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        nameSizeVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleName, font=(nameFontVariable.get(), nameSizeVariable.get(), getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        self.nameBoldVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleName, font=(nameFontVariable.get(), nameSizeVariable.get(), getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        self.nameItalicVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleName, font=(nameFontVariable.get(), nameSizeVariable.get(), getModifiers(self.nameBoldVariable.get(), self.nameItalicVariable.get()))))
        nameColorVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(exampleName, fill=nameColorVariable.get()))
        nameAnchorXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleName, anchor=getAnchor(nameAnchorXVariable.get(), nameAnchorYVariable.get()),
            justify=getJustify(getAnchor(nameAnchorXVariable.get(), nameAnchorYVariable.get()))))
        nameAnchorYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleName, anchor=getAnchor(nameAnchorXVariable.get(), nameAnchorYVariable.get()),
            justify=getJustify(getAnchor(nameAnchorXVariable.get(), nameAnchorYVariable.get()))))
        nameXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleName, cleverInt(nameXVariable.get()), cleverInt(nameYVariable.get())))
        nameYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleName, cleverInt(nameXVariable.get()), cleverInt(nameYVariable.get())))
        textFontVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleText, font=(textFontVariable.get(), textSizeVariable.get(), getModifiers(self.textBoldVariable.get(), self.textItalicVariable.get()))))
        textSizeVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleText, font=(textFontVariable.get(), textSizeVariable.get(), getModifiers(self.textBoldVariable.get(), self.textItalicVariable.get()))))
        textColorVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(exampleText, fill=textColorVariable.get()))
        self.textBoldVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleText, font=(textFontVariable.get(), textSizeVariable.get(), getModifiers(self.textBoldVariable.get(), self.textItalicVariable.get()))))
        self.textItalicVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleText, font=(textFontVariable.get(), textSizeVariable.get(), getModifiers(self.textBoldVariable.get(), self.textItalicVariable.get()))))
        textAnchorXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleText, anchor=getAnchor(textAnchorXVariable.get(), textAnchorYVariable.get()),
            justify=getJustify(getAnchor(textAnchorXVariable.get(), textAnchorYVariable.get()))))
        textAnchorYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleText, anchor=getAnchor(textAnchorXVariable.get(), textAnchorYVariable.get()),
            justify=getJustify(getAnchor(textAnchorXVariable.get(), textAnchorYVariable.get()))))
        textXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleText, cleverInt(textXVariable.get()), cleverInt(textYVariable.get())))
        textYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleText, cleverInt(textXVariable.get()), cleverInt(textYVariable.get())))
        resultFontVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleResult, font=(resultFontVariable.get(), resultSizeVariable.get(), getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        resultSizeVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleResult, font=(resultFontVariable.get(), resultSizeVariable.get(), getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        self.resultBoldVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleResult, font=(resultFontVariable.get(), resultSizeVariable.get(), getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        self.resultItalicVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleResult, font=(resultFontVariable.get(), resultSizeVariable.get(), getModifiers(self.resultBoldVariable.get(), self.resultItalicVariable.get()))))
        resultColorVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(exampleResult, fill=resultColorVariable.get()))
        resultAnchorXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleResult, anchor=getAnchor(resultAnchorXVariable.get(), resultAnchorYVariable.get()),
            justify=getJustify(getAnchor(resultAnchorXVariable.get(), resultAnchorYVariable.get()))))
        resultAnchorYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.itemconfig(
            exampleResult, anchor=getAnchor(resultAnchorXVariable.get(), resultAnchorYVariable.get()),
            justify=getJustify(getAnchor(resultAnchorXVariable.get(), resultAnchorYVariable.get()))))
        resultXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleResult, cleverInt(resultXVariable.get()), cleverInt(resultYVariable.get())))
        resultYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleResult, cleverInt(resultXVariable.get()), cleverInt(resultYVariable.get())))
        flagHeightVariable.trace_add('write', lambda var, index, mode: self.updateFlag(
            exampleCanvas, exampleFlagImage, cleverInt(flagHeightVariable.get())))
        flagXVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleFlagImage, cleverInt(flagXVariable.get()), cleverInt(flagYVariable.get())))
        flagYVariable.trace_add('write', lambda var, index, mode: exampleCanvas.coords(
            exampleFlagImage, cleverInt(flagXVariable.get()), cleverInt(flagYVariable.get())))
        avatarWidthVariable.trace_add('write', lambda var, index, mode: self.updateAvatar(
            exampleCanvas, exampleAvatarImage, cleverInt(avatarXVariable.get()), cleverInt(avatarYVariable.get()), cleverInt(avatarWidthVariable.get()), cleverInt(avatarHeightVariable.get()), exampleAvatarRectangle))
        avatarHeightVariable.trace_add('write', lambda var, index, mode: self.updateAvatar(
            exampleCanvas, exampleAvatarImage, cleverInt(avatarXVariable.get()), cleverInt(avatarYVariable.get()), cleverInt(avatarWidthVariable.get()), cleverInt(avatarHeightVariable.get()), exampleAvatarRectangle))
        avatarXVariable.trace_add('write', lambda var, index, mode: self.updateAvatar(
            exampleCanvas, exampleAvatarImage, cleverInt(avatarXVariable.get()), cleverInt(avatarYVariable.get()), cleverInt(avatarWidthVariable.get()), cleverInt(avatarHeightVariable.get()), exampleAvatarRectangle))
        avatarYVariable.trace_add('write', lambda var, index, mode: self.updateAvatar(
            exampleCanvas, exampleAvatarImage, cleverInt(avatarXVariable.get()), cleverInt(avatarYVariable.get()), cleverInt(avatarWidthVariable.get()), cleverInt(avatarHeightVariable.get()), exampleAvatarRectangle))

        self.enableButtonCallback(self.flagEnable, [flagHeightSpinbox, flagXSpinbox, flagYSpinbox], exampleCanvas, [exampleFlagImage])
        self.enableButtonCallback(self.avatarEnable,
                                  [avatarWidthSpinbox, avatarHeightSpinbox, avatarXSpinbox, avatarYSpinbox], exampleCanvas, [exampleAvatarImage, exampleAvatarRectangle])
        backgroundColorVariable.trace_add('write', lambda var, index, mode: exampleCanvas.configure(background=backgroundColorVariable.get()))

    def updateFPSCloseButton(self, FPS, window):
        self.FPS = FPS
        window.destroy()
        self.settingsChanged.set(True)

    def updateFPS(self):
        FPSWindow = tk.Toplevel(self.root)
        FPSWindow.grab_set()
        FPSWindow.rowconfigure(0, pad=20)
        FPSWindow.rowconfigure(1, pad=20)
        FPSWindow.rowconfigure(2, pad=20)
        FPSTitle = tk.Label(FPSWindow, text='FPS for intro/loop/outro videos.\nBe careful, setting FPS too high may make the app laggy.')
        FPSTitle.grid(column=0, columnspan=2, row=0)
        FPSLabel = tk.Label(FPSWindow, text='FPS:')
        FPSLabel.grid(column=0, row=1, sticky='e')
        FPSVariable = tk.StringVar()
        FPSSpinbox = tk.Spinbox(FPSWindow, width=20, from_=0, to=50, textvariable=FPSVariable)
        FPSSpinbox.grid(column=1, row=1, sticky='w')
        FPSVariable.set(f'{self.FPS}')
        OKButton = tk.Button(FPSWindow, text='OK', command=lambda: self.updateFPSCloseButton(cleverInt(FPSVariable.get()), FPSWindow))
        OKButton.grid(column=0, columnspan=2, row=2)

    def updateTelegramSettingsCloseButton(self, token, id, window):
        self.botToken = token
        self.botChannelId = id
        try:
            if self.bot is None:
                self.bot = TelegramBot.TelegramBot(self.botToken, self.botChannelId, False, True)
                self.bot.sendSimpleMessage('Bot Cards ready')
                self.bot.setMessageHandler(['cardData'], self.dataCallback)
                self.bot.setMessageHandler(['cardResult'], self.resultCallback)
                self.threadBot = threading.Thread(target=self.bot.startPolling)
                self.threadBot.daemon = True
                self.threadBot.start()
        except:
            tkinter.messagebox.showerror(
                title='Bot Error !', message='Telegram Bot Error ! Please make sure the Settings are correct')
        else:
            window.destroy()
            self.settingsChanged.set(True)

    def updateTelegramSettings(self):
        telegramWindow = tk.Toplevel(self.root)
        telegramWindow.grab_set()
        telegramLabel = tk.Label(telegramWindow, text='Please enter Telegram settings')
        telegramLabel.pack(pady=20)
        tokenLabel = tk.Label(telegramWindow, text='Cards bot token')
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

    def prepareWithRequest(self, i):
        canvas = self.canvases[i]
        name = self.names[i]
        text = self.texts[i]
        result = self.results[i]
        flagImage = self.flagImages[i]
        avatarImage = self.avatarImages[i]
        if self.flagEnable:
            self.flags[i] = Image.getFlag(self.flagHeight, self.requestCountries[i])
            canvas.itemconfig(flagImage, image=self.flags[i])
        if self.avatarEnable:
            self.avatars[i] = Image.getAvatar(self.avatarWidth, self.avatarHeight, self.requestAvatars[i])
            canvas.itemconfig(avatarImage, image=self.avatars[i])
        canvas.itemconfig(name, text=self.requestNames[i])
        canvas.itemconfig(text, text=self.requestTexts[i])
        canvas.itemconfig(result, text=self.requestResults[i])

    def show(self, i):
        canvas = self.canvases[i]
        background = self.backgrounds[i]
        name = self.names[i]
        text = self.texts[i]
        result = self.results[i]
        flagImage = self.flagImages[i]
        avatarImage = self.avatarImages[i]
        canvas.itemconfig(background, state='normal')
        if self.flagEnable:
            canvas.itemconfig(flagImage, state='normal')
        if self.avatarEnable:
            canvas.itemconfig(avatarImage, state='normal')
        canvas.itemconfig(name, state='normal')
        canvas.itemconfig(text, state='normal')
        canvas.itemconfig(result, state='normal')
        canvas.update()

    def hide(self, i):
        canvas = self.canvases[i]
        name = self.names[i]
        text = self.texts[i]
        result = self.results[i]
        flagImage = self.flagImages[i]
        avatarImage = self.avatarImages[i]
        canvas.itemconfig(flagImage, state='hidden')
        canvas.itemconfig(avatarImage, state='hidden')
        canvas.itemconfig(name, state='hidden')
        canvas.itemconfig(text, state='hidden')
        canvas.itemconfig(result, state='hidden')
        canvas.update()

    def checkAllQueues(self):
        if self.reloadCards[0]:
            self.cardsInit(self.reloadCards[1], self.reloadCards[2])
            self.reloadCards = (False, 1, 1)
        start = time.time()
        for i in range(0, self.camerasCount):
            dataQueue = self.dataQueues[i]
            resultQueue = self.resultQueues[i]
            canvas = self.canvases[i]
            background = self.backgrounds[i]
            backgroundState = self.backgroundStates[i]
            nextBackgroundState = backgroundState
            index = self.backgroundIndices[i]
            nextIndex = index

            # Update background
            if backgroundState == cardsUtils.BackgroundState.EMPTY:
                canvas.itemconfig(background, state='hidden')
            else:
                image = None
                match backgroundState:
                    case cardsUtils.BackgroundState.INTRO:
                        image = self.introImages[index]
                    case cardsUtils.BackgroundState.LOOP:
                        if self.loopFile != '':
                            image = self.loopImages[index]
                    case cardsUtils.BackgroundState.OUTRO:
                        image = self.outroImages[index]
                if image is not None:
                    canvas.itemconfig(background, image=image, state='normal')
                    canvas.update()

            # Get new requests from queues
            try:
                (self.requestCountries[i], self.requestNames[i], self.requestAvatars[i], self.requestTexts[i]) = dataQueue.get(block=False)
                if self.requestNames[i] != '':
                    self.prepareWithRequest(i)
            except queue.Empty:
                pass

            try:
                self.requestResults[i] = resultQueue.get(block=False)
                if self.requestResults[i] != '':
                    self.prepareWithRequest(i)
            except queue.Empty:
                pass

            # Update state if needed
            match backgroundState:
                case cardsUtils.BackgroundState.EMPTY:
                    if self.requestNames[i] != '':
                        if self.introFile != '':
                            nextBackgroundState = cardsUtils.BackgroundState.INTRO
                        else:
                            nextBackgroundState = cardsUtils.BackgroundState.LOOP
                            self.show(i)
                        nextIndex = 0
                case cardsUtils.BackgroundState.INTRO:
                    if index == len(self.introImages) - 1:
                        nextIndex = 0
                        nextBackgroundState = cardsUtils.BackgroundState.LOOP
                        self.show(i)
                    else:
                        nextIndex = index + 1
                case cardsUtils.BackgroundState.LOOP:
                    if self.requestNames[i] == '':
                        if self.outroFile != '':
                            nextBackgroundState = cardsUtils.BackgroundState.OUTRO
                        else:
                            nextBackgroundState = cardsUtils.BackgroundState.EMPTY
                        self.hide(i)
                        nextIndex = 0
                    else:
                        if index == len(self.loopImages) - 1:
                            nextIndex = 0
                        else:
                            nextIndex = index + 1
                case cardsUtils.BackgroundState.OUTRO:
                    if index == len(self.outroImages) - 1:
                        nextIndex = 0
                        nextBackgroundState = cardsUtils.BackgroundState.EMPTY
                    else:
                        nextIndex = index + 1
            self.backgroundStates[i] = nextBackgroundState
            self.backgroundIndices[i] = nextIndex
        delay = max(0, int(1000 / self.FPS - 1000 * (time.time() - start)))
        self.root.after(delay, self.checkAllQueues)

    def showSettingsFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black', highlightthickness=1)
        settingsLabel = tk.Label(frame, text='Cards Settings', bg=self.BG_COLOR)
        settingsLabel.grid(column=0, row=0)
        cameraButton = tk.Button(frame, text='Update cameras', command=self.updateCameras)
        cameraButton.grid(column=0, row=1)
        layoutButton = tk.Button(frame, text='Update layout', command=self.updateLayout)
        layoutButton.grid(column=0, row=2)
        FPSButton = tk.Button(frame, text='Change FPS for videos', command=self.updateFPS)
        FPSButton.grid(column=0, row=3)
        telegramButton = tk.Button(frame, text='Change Telegram Settings', command=self.updateTelegramSettings)
        telegramButton.grid(column=0, row=4)
        saveButton = tk.Button(frame, text='Save Cards Settings...', command=self.saveSettings)
        saveButton.grid(column=0, row=5)
        saveButton = tk.Button(frame, text='Load Cards Settings...', command=self.loadSettings)
        saveButton.grid(column=0, row=6)
        frame.pack(side=tk.LEFT, fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
        frame.rowconfigure(4, pad=20)
        frame.rowconfigure(5, pad=20)
        frame.rowconfigure(6, pad=20)
