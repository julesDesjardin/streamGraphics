import tkinter as tk
from tkinter import ttk
import json
import dataWrite
import WCIFParse
import InterfaceSettings
import utils


class PresentationInterface:
    def __init__(self, root, wcif, text, venue, room, event, round, group, bot):

        self.root = root
        self.wcif = wcif
        self.text = text
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
                wcif, x, event, utils.SEED_TYPE[utils.EVENTS[event]], 'world'), reverse=True)
        else:
            self.competitorsId.sort(key=lambda x: WCIFParse.getRoundResult(
                wcif, x, event, round - 1, utils.SEED_TYPE[utils.EVENTS[event]]), reverse=True)

        self.avatars = []
        self.competitorsName = []
        for competitor in self.competitorsId:
            self.avatars.append(WCIFParse.getAvatar(wcif, competitor))
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
            dataWrite.sendCardData(self.bot, 0, '', '', '', '', True)
        else:
            dataWrite.sendCardData(self.bot, 0, WCIFParse.getCountry(self.wcif, self.competitorsId[self.id]), self.competitorsName[self.id], self.avatars[self.id], utils.replaceText(
                self.text, self.wcif, self.competitorsId[self.id], len(self.competitorsId) - self.id, self.event, self.round), True)

    def previousButtonCommand(self):
        self.id = self.id - 1
        self.updateButtons()

    def nextButtonCommand(self):
        if self.id == len(self.competitorsId) - 1:
            dataWrite.sendCardData(self.bot, 0, '', '', '', '', True)
            self.window.destroy()
        else:
            self.id = self.id + 1
            self.updateButtons()
