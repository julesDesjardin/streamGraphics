import tkinter as tk
from tkinter import ttk
import json
import dataWrite
import WCIFParse
import interfaceUtils

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot
from Common.commonUtils import COUNTRIES


class PresentationInterface:
    def __init__(self, root, wcif, text, region, venue, room, event, round, group, bot):

        self.root = root
        self.wcif = wcif
        self.text = text
        self.region = region
        self.event = event
        self.round = round
        self.bot = bot
        self.window = tk.Toplevel(self.root)
        self.window.geometry('500x500')
        self.window.grab_set()

        self.id = -1
        activityId = WCIFParse.getActivityId(wcif, venue, room, event, round, group)

        foreignCompetitors = [competitor for competitor in WCIFParse.getCompetitors(wcif, activityId, event)
                              if self.region != 'World' and self.region not in COUNTRIES[WCIFParse.getCountry(self.wcif, competitor[0])]]
        localCompetitors = [competitor for competitor in WCIFParse.getCompetitors(wcif, activityId, event)
                            if self.region == 'World' or self.region in COUNTRIES[WCIFParse.getCountry(self.wcif, competitor[0])]]
        foreignCompetitors.sort(key=lambda x: self.getKey(x[0]), reverse=True)
        localCompetitors.sort(key=lambda x: self.getKey(x[0]), reverse=True)

        # This is an array of tuple: for each element, competitor[0] is the ID and competitor[1] is the seed
        self.competitors = foreignCompetitors + localCompetitors

        self.avatars = []
        self.competitorsName = []
        self.seeds = []
        for competitor in self.competitors:
            self.avatars.append(WCIFParse.getAvatar(wcif, competitor[0]))
            self.competitorsName.append(WCIFParse.getCompetitorName(wcif, competitor[0]))

        self.previousButton = tk.Button(self.window, command=self.previousButtonCommand)
        self.previousButton.pack(pady=20, anchor='n')

        self.currentLabel = tk.Label(self.window)
        self.currentLabel.pack(pady=20, anchor='n')

        self.nextButton = tk.Button(self.window, command=self.nextButtonCommand)
        self.nextButton.pack(pady=20, anchor='n')

        self.quitButton = tk.Button(self.window, text='Quit', command=self.window.destroy)
        self.quitButton.pack(pady=20, side='bottom')

        self.updateButtons()

    def getKey(self, id):
        if self.round == 1:
            return WCIFParse.getRanking(self.wcif, id, self.event, interfaceUtils.SEED_TYPE[interfaceUtils.EVENTS[self.event]], 'world')
        else:
            return WCIFParse.getRoundResult(self.wcif, id, self.event, self.round - 1, interfaceUtils.SEED_TYPE[interfaceUtils.EVENTS[self.event]])

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

        if self.id == len(self.competitors) - 1:
            self.nextButton.configure(text='Close presentation')
        else:
            self.nextButton.configure(text=f'Next: {self.competitorsName[self.id + 1]}')

        if self.id == -1:
            dataWrite.sendCardData(self.bot, 0, '', '', '', '', True)
        else:
            dataWrite.sendCardData(self.bot, 0, WCIFParse.getCountry(self.wcif, self.competitors[self.id][0]), self.competitorsName[self.id], self.avatars[self.id], interfaceUtils.replaceText(
                self.text, self.wcif, self.competitors[self.id][0], self.competitors[self.id][1], self.event, self.round), True)

    def previousButtonCommand(self):
        self.id = self.id - 1
        self.updateButtons()

    def nextButtonCommand(self):
        if self.id == len(self.competitors) - 1:
            dataWrite.sendCardData(self.bot, 0, '', '', '', '', True)
            self.window.destroy()
        else:
            self.id = self.id + 1
            self.updateButtons()
