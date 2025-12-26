import tkinter as tk
import tkinter.messagebox
import interfaceUtils
import dataWrite
import WCIFParse


class InterfaceFrame:

    def __init__(self, root, wcif, cardText, customTexts, customImages, bot, buttonRows, buttonCols, x, y, index):

        self.emptyPixel = tk.PhotoImage(width=1, height=1)

        self.root = root
        self.wcif = wcif
        self.cardText = cardText
        self.customTexts = customTexts
        self.customImages = customImages
        self.bot = bot
        self.buttonRows = buttonRows
        self.buttonCols = buttonCols
        self.x = x
        self.y = y
        self.index = index
        self.activeCuber = -1

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
                                   command=lambda: self.buttonCommand(-1, '', '', '', '', -1))
        self.cleanButton.grid(column=0, row=1, columnspan=self.buttonCols)

        self.buttonFrames = []
        self.buttons = []
        for button in range(0, self.buttonCols + 2):
            self.frame.columnconfigure(button, pad=interfaceUtils.BUTTON_PADX)
        for button in range(0, self.buttonRows):
            self.frame.rowconfigure(button, pad=interfaceUtils.BUTTON_PADY)

        for button in range(0, self.buttonCols * self.buttonRows):
            self.buttonFrames.append(tk.Frame(self.frame, highlightthickness=interfaceUtils.BUTTON_THICKNESS))
            self.buttons.append(tk.Button(self.buttonFrames[-1], image=self.emptyPixel,
                                compound='c', width=interfaceUtils.BUTTON_WIDTH, height=interfaceUtils.BUTTON_HEIGHT, anchor=tk.W, justify=tk.LEFT))
            self.buttons[-1].pack()

    def buttonCommand(self, buttonIndex, country, name, avatar, cardText, competitorId):
        for index in range(len(self.buttons)):
            if index == buttonIndex:
                self.buttonFrames[index].configure(highlightbackground='black')
                self.buttons[index].configure(relief=tk.SUNKEN)
            else:
                self.buttonFrames[index].configure(highlightbackground='white')
                self.buttons[index].configure(relief=tk.RAISED)
        dataWrite.sendCardData(self.bot, self.index, country, name.split('(')[0].strip(), avatar, cardText, False)
        self.activeCuber = competitorId

    def configureButton(self, buttonIndex, event, round, competitor, visible, row, column, bg, fg):
        if not visible:
            self.buttonFrames[buttonIndex].grid_forget()
        else:
            if int(round) > 1:
                previousRound = int(round) - 1
            else:
                previousRound = None
            id = competitor[0]
            seed = competitor[1]
            name = competitor[2]
            previousRank = WCIFParse.getRoundRank(self.wcif, id, event, previousRound)
            extraButtonText = f'Seed {seed}'
            if previousRank is not None:
                extraButtonText = extraButtonText + f', Placed {previousRank}'
            cardTextReplaced = interfaceUtils.replaceText(self.cardText, self.wcif, id, seed, event, round, self.customTexts)
            WCAID = WCIFParse.getWCAID(self.wcif, id)
            if WCAID in self.customImages:
                avatar = self.customImages[WCAID]
            else:
                avatar = WCIFParse.getAvatar(self.wcif, id)
            self.buttons[buttonIndex].configure(text=f'{name}\n{extraButtonText}', bg=bg, fg=fg, command=lambda: self.buttonCommand(
                buttonIndex, WCIFParse.getCountry(self.wcif, id), name, avatar, cardTextReplaced, id))
            self.buttonFrames[buttonIndex].grid(row=row, column=column)

    def showFrame(self):
        self.frame.grid(column=self.x, row=self.y)

    def hideFrame(self):
        self.frame.grid_forget()
