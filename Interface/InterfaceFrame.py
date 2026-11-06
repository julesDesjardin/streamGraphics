import tkinter as tk
import tkinter.messagebox
from . import interfaceUtils
from . import WCIFParse
from Common import TelegramBot, commonUtils


class InterfaceFrame:

    def __init__(self, root, wcif, datastream, region, customTexts, customImages, buttonRows, buttonCols, x, y, index):

        self.emptyPixel = tk.PhotoImage(width=1, height=1)

        self.root = root
        self.wcif = wcif
        self.datastream = datastream
        self.region = region
        self.customTexts = customTexts
        self.customImages = customImages
        self.buttonRows = buttonRows
        self.buttonCols = buttonCols
        self.x = x
        self.y = y
        self.index = index
        self.activeCuber = ''
        self.fullResults = dict([])

        frameWidth = 2 * interfaceUtils.FRAME_THICKNESS + (self.buttonCols + 1) * \
            (interfaceUtils.BUTTON_WIDTH + 2 * interfaceUtils.BUTTON_PADX + 2 * interfaceUtils.BUTTON_THICKNESS + 3)
        frameHeight = 2 * interfaceUtils.FRAME_THICKNESS + interfaceUtils.LABEL_HEIGHT + \
            (self.buttonRows + 2) * (interfaceUtils.BUTTON_HEIGHT + 2 * interfaceUtils.BUTTON_PADY + 2 * interfaceUtils.BUTTON_THICKNESS + 3)
        self.frame = tk.Frame(self.root, highlightbackground='black',
                              highlightthickness=interfaceUtils.FRAME_THICKNESS, width=frameWidth, height=frameHeight)
        self.frame.grid_propagate(0)
        self.frame.grid_rowconfigure(0, minsize=interfaceUtils.LABEL_HEIGHT)

        self.label = tk.Label(self.frame, text=f'Cuber on camera {index+1}')
        self.label.grid(column=0, row=0, columnspan=self.buttonCols)

        self.cleanButton = tk.Button(self.frame)
        self.cleanButton.configure(text=f'Clean', image=self.emptyPixel, compound='c', width=interfaceUtils.BUTTON_WIDTH, height=interfaceUtils.BUTTON_HEIGHT,
                                   command=lambda: self.buttonCommand(-1, '', '', '', ''))
        self.cleanButton.grid(column=0, row=1, columnspan=self.buttonCols)

        self.buttonFrames = []
        self.buttons = []
        self.buttonsActive = []
        self.countries = []
        for button in range(0, self.buttonCols + 2):
            self.frame.columnconfigure(button, pad=interfaceUtils.BUTTON_PADX)
        for button in range(0, self.buttonRows):
            self.frame.rowconfigure(button, pad=interfaceUtils.BUTTON_PADY)

        for button in range(0, self.buttonCols * self.buttonRows):
            self.buttonFrames.append(tk.Frame(self.frame, highlightthickness=interfaceUtils.BUTTON_THICKNESS))
            self.buttons.append(tk.Button(self.buttonFrames[-1], image=self.emptyPixel,
                                compound='c', width=interfaceUtils.BUTTON_WIDTH, height=interfaceUtils.BUTTON_HEIGHT, anchor=tk.W, justify=tk.LEFT))
            self.buttonsActive.append(False)
            self.countries.append('')
            self.buttons[-1].pack()

    def buttonCommand(self, buttonIndex, id, event, round, seed):
        for index in range(len(self.buttons)):
            if index == buttonIndex:
                self.buttonFrames[index].configure(highlightbackground='black')
                self.buttons[index].configure(relief=tk.SUNKEN)
            else:
                self.buttonFrames[index].configure(highlightbackground='white')
                self.buttons[index].configure(relief=tk.RAISED)

        if buttonIndex == -1:
            return

        # Get info to write to the card
        payload = {}
        if int(round) > 1:
            previousRound = int(round) - 1
        else:
            previousRound = None
        payload['previousRank'] = WCIFParse.getRoundRank(self.wcif, id, event, previousRound)
        WCAID = WCIFParse.getWCAID(self.wcif, id)
        payload['WCAID'] = WCAID
        payload['name'] = WCIFParse.getCompetitorName(self.wcif, id)
        country = WCIFParse.getCountry(self.wcif, id)
        payload['countryFlag'] = commonUtils.getFlagURL(country)
        payload['prSingle'] = interfaceUtils.resultToString(WCIFParse.getPb(self.wcif, id, event, 'single'))
        payload['prAverage'] = interfaceUtils.resultToString(WCIFParse.getPb(self.wcif, id, event, 'average'))
        if self.region == 'World':
            payload['rankingSingle'] = f"WR: {WCIFParse.getRanking(self.wcif, id, event, 'single', 'world')}"
            payload['rankingAverage'] = f"WR: {WCIFParse.getRanking(self.wcif, id, event, 'average', 'world')}"
        elif self.region in commonUtils.CONTINENTS:
            if commonUtils.COUNTRIES[country][1] == self.region:
                payload['rankingSingle'] = f"CR: {WCIFParse.getRanking(self.wcif, id, event, 'single', 'continental')}"
                payload['rankingAverage'] = f"CR: {WCIFParse.getRanking(self.wcif, id, event, 'average', 'continental')}"
            else:
                payload['rankingSingle'] = f"WR: {WCIFParse.getRanking(self.wcif, id, event, 'single', 'world')}"
                payload['rankingAverage'] = f"WR: {WCIFParse.getRanking(self.wcif, id, event, 'average', 'world')}"
        else:
            if commonUtils.COUNTRIES[country][0] == self.region:
                payload['rankingSingle'] = f"NR: {WCIFParse.getRanking(self.wcif, id, event, 'single', 'national')}"
                payload['rankingAverage'] = f"NR: {WCIFParse.getRanking(self.wcif, id, event, 'average', 'national')}"
            else:
                payload['rankingSingle'] = f"WR: {WCIFParse.getRanking(self.wcif, id, event, 'single', 'world')}"
                payload['rankingAverage'] = f"WR: {WCIFParse.getRanking(self.wcif, id, event, 'average', 'world')}"
        payload['seed'] = seed
        payload['previousSingle'] = interfaceUtils.resultToString(WCIFParse.getRoundResult(self.wcif, id, event, previousRound, 'single'))
        payload['previousAverage'] = interfaceUtils.resultToString(WCIFParse.getRoundResult(self.wcif, id, event, previousRound, 'average'))
        if WCAID in self.customTexts[interfaceUtils.EVENTS[event]]:
            payload['fact'] = self.customTexts[interfaceUtils.EVENTS[event]][WCAID]
        else:
            payload['fact'] = ''
        if WCAID in self.customImages:
            payload['image'] = self.customImages[WCAID]
        else:
            payload['image'] = WCIFParse.getAvatar(self.wcif, id)

        commonUtils.sendPayload(self.datastream, payload)

    def configureButton(self, buttonIndex, event, round, competitor, visible, row, column, bg, fg):
        if not visible:
            self.buttonFrames[buttonIndex].grid_forget()
            self.buttonsActive[buttonIndex] = False
        else:
            if int(round) > 1:
                previousRound = int(round) - 1
            else:
                previousRound = None
            id = competitor[0]
            seed = competitor[1]
            name = competitor[2]
            country = WCIFParse.getCountry(self.wcif, id)
            previousRank = WCIFParse.getRoundRank(self.wcif, id, event, previousRound)
            extraButtonText = f'Seed {seed}'
            if previousRank is not None:
                extraButtonText = extraButtonText + f', Placed {previousRank}'
            self.buttons[buttonIndex].configure(text=f'{name}\n{extraButtonText}', bg=bg, fg=fg,
                                                command=lambda: self.buttonCommand(buttonIndex, id, event, round, seed))
            self.buttonFrames[buttonIndex].grid(row=row, column=column)
            self.buttonsActive[buttonIndex] = True
            self.countries[buttonIndex] = country

    def showFrame(self):
        self.frame.grid(column=self.x, row=self.y)

    def hideFrame(self):
        self.frame.grid_forget()
