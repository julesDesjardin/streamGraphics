import tkinter as tk
from tkinter import ttk
import json
import dataWrite
import WCIFParse
import InterfaceSettings
import constants


class PresentationInterface:
    def __init__(self, root, wcif, venue, room, event, round, group, bot):

        self.root = root
        self.event = event
        self.round = round
        self.bot = bot
        self.window = tk.Toplevel(self.root)
        self.window.geometry('500x500')
        self.window.grab_set()

        self.id = -1
        activityId = WCIFParse.getActivityId(wcif, venue, room, event, round, group)
        self.competitorsId = [competitor[0] for competitor in WCIFParse.getCompetitors(wcif, activityId, event)]
        if round == 1:
            self.competitorsId.sort(key=lambda x: WCIFParse.getRanking(
                wcif, x, event, constants.SEED_TYPE[constants.EVENTS[event]], 'world'), reverse=True)
        else:
            self.competitorsId.sort(key=lambda x: WCIFParse.getRoundResult(
                wcif, x, event, round - 1, constants.SEED_TYPE[constants.EVENTS[event]]), reverse=True)

        self.competitorsWCAID = []
        self.competitorsName = []
        for competitor in self.competitorsId:
            self.competitorsWCAID.append(WCIFParse.getWCAID(wcif, competitor))
            self.competitorsName.append(WCIFParse.getCompetitorName(wcif, competitor))

        self.previousButton = tk.Button(self.window, command=self.previousButtonCommand)
        self.previousButton.pack(pady=20, anchor='n')

        self.currentLabel = tk.Label(self.window)
        self.currentLabel.pack(pady=20, anchor='n')

        self.nextButton = tk.Button(self.window, command=self.nextButtonCommand)
        self.nextButton.pack(pady=20, anchor='n')

        self.quitButton = tk.Button(self.window, text='Quit', command=self.window.destroy)
        self.quitButton.pack(pady=20, side='bottom')

        self.updateButtons()

    def updateButtons(self):
        if self.id == -1:
            self.previousButton.configure(state='disabled', text='Previous: no previous competitor')
        elif self.id == 0:
            self.previousButton.configure(state='active', text='No previous competitor, Remove presentation')
        else:
            self.previousButton.configure(state='active', text=f'Previous: {self.competitorsName[self.id - 1]}')

        if self.id == -1:
            self.currentLabel.configure(text='No presentation currently shown')
        else:
            self.currentLabel.configure(text=f'Current presentation: {self.competitorsName[self.id]}')

        if self.id == len(self.competitorsId) - 1:
            self.nextButton.configure(text='Close presentation')
        else:
            self.nextButton.configure(text=f'Next: {self.competitorsName[self.id + 1]}')

        if self.id == -1:
            self.bot.sendSimpleMessage('/presentation ')
        else:
            self.bot.sendSimpleMessage(f'/presentation {self.event} {self.round} {self.id} {self.competitorsWCAID[self.id]}')

    def previousButtonCommand(self):
        self.id = self.id - 1
        self.updateButtons()

    def nextButtonCommand(self):
        if self.id == len(self.competitorsId) - 1:
            self.bot.sendSimpleMessage('/presentation ')
            self.window.destroy()
        else:
            self.id = self.id + 1
            self.updateButtons()
