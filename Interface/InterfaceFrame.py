import tkinter as tk
import tkinter.messagebox
import utils
import dataWrite
import WCIFParse


class InterfaceFrame:

    def __init__(self, root, wcif, bot, buttonRows, buttonCols, x, y, index):

        self.emptyPixel = tk.PhotoImage(width=1, height=1)

        self.root = root
        self.wcif = wcif
        self.bot = bot
        self.buttonRows = buttonRows
        self.buttonCols = buttonCols
        self.x = x
        self.y = y
        self.index = index
        self.activeCuber = -1

        frameWidth = 2 * utils.FRAME_THICKNESS + self.buttonCols * (utils.BUTTON_WIDTH + 2 * utils.BUTTON_PADX + 2 * utils.BUTTON_THICKNESS + 3)
        frameHeight = 2 * utils.FRAME_THICKNESS + utils.LABEL_HEIGHT + \
            (self.buttonRows + 2) * (utils.BUTTON_HEIGHT + 2 * utils.BUTTON_PADY + 2 * utils.BUTTON_THICKNESS + 3)
        self.frame = tk.Frame(self.root, highlightbackground='black', highlightthickness=utils.FRAME_THICKNESS, width=frameWidth, height=frameHeight)
        self.frame.grid_propagate(0)
        self.frame.grid_rowconfigure(0, minsize=utils.LABEL_HEIGHT)

        self.label = tk.Label(self.frame, text=f'Cuber on camera {index+1}')
        self.label.grid(column=0, row=0, columnspan=self.buttonCols)

        self.timeTowerVariable = tk.IntVar()
        self.timeTowerButton = tk.Checkbutton(self.frame, text='Expand TimeTower line',
                                              variable=self.timeTowerVariable, command=self.timeTowerCommand)
        self.timeTowerButton.grid(column=0, row=1, columnspan=self.buttonCols)

        self.cleanButton = tk.Button(self.frame)
        self.cleanButton.configure(text=f'Clean', image=self.emptyPixel, compound='c', width=utils.BUTTON_WIDTH, height=utils.BUTTON_HEIGHT,
                                   command=lambda: self.buttonCommand(-1, '', '', '', '', -1))
        self.cleanButton.grid(column=0, row=2, columnspan=self.buttonCols)

        self.buttonFrames = []
        self.buttons = []
        for button in range(0, self.buttonCols + 2):
            self.frame.columnconfigure(button, pad=utils.BUTTON_PADX)
        for button in range(0, self.buttonRows):
            self.frame.rowconfigure(button, pad=utils.BUTTON_PADY)

        for button in range(0, self.buttonCols * self.buttonRows):
            self.buttonFrames.append(tk.Frame(self.frame, highlightthickness=utils.BUTTON_THICKNESS))
            self.buttons.append(tk.Button(self.buttonFrames[-1], image=self.emptyPixel,
                                compound='c', width=utils.BUTTON_WIDTH, height=utils.BUTTON_HEIGHT, anchor=tk.W, justify=tk.LEFT))
            self.buttons[-1].pack()

    def timeTowerCommand(self):
        dataWrite.sendTimeTowerExpand(self.bot, WCIFParse.getRegistrantId(self.wcif, activeCuber), timeTowerVariable.get())

    def buttonCommand(self, buttonIndex, country, name, avatar, cardText, competitorId):
        for index in range(len(self.buttons)):
            if index == buttonIndex:
                self.buttonFrames[index].configure(highlightbackground='black')
                self.buttons[index].configure(relief=tk.SUNKEN)
            else:
                self.buttonFrames[index].configure(highlightbackground='white')
                self.buttons[index].configure(relief=tk.RAISED)
        dataWrite.sendCardData(self.bot, self.index, country, name, avatar, cardText, False)
        if self.timeTowerVariable.get() == 1:
            dataWrite.sendTimeTowerExpand(self.bot, WCIFParse.getRegistrantId(self.wcif, self.activeCuber), 0)
            dataWrite.sendTimeTowerExpand(self.bot, WCIFParse.getRegistrantId(self.wcif, competitorId), 1)
        self.activeCuber = competitorId

    def showFrame(self):
        self.frame.grid(column=self.x, row=self.y)

    def hideFrame(self):
        self.frame.grid_forget()
