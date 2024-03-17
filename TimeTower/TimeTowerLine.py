import tkinter as tk
from tkinter import ttk
import json
import utils

class TimeTowerLine:

    def __init__(self, canvas, widthName, widthResults, height, roundId, competitorId, country, name, criteria):
        self.canvas = canvas
        self.widthName = widthName
        self.widthResults = widthResults
        self.height = height
        self.roundId = roundId
        self.competitorId = competitorId
        self.country = country
        self.fullName = name.split('(')[0].strip() # Removes part in parentheses (could mess up the display, + messes up the 3 letter name) + trailing space in this case
        fullNameSplit = self.fullName.split(' ')
        self.smallName = (fullNameSplit[0][0] + '. ' + fullNameSplit[-1][0:3]).upper()
        self.criteria = criteria
        self.results = []
        self.currentResult = 0
        self.ranking = 0

    def updateResults(self, queryResult):
        for result in queryResult['round']['results']:
            if result['person']['id'] == self.competitorId:
                self.results = []
                for attempt in result['attempts']:
                    if attempt['result'] < 0:
                        nonDNFResult = utils.MAX_RESULT
                    else:
                        nonDNFResult = attempt['result']
                    self.results.append(nonDNFResult)
        
        # Update currentResult
        if len(self.results) == 0:
            self.currentResult = utils.MAX_RESULT
        else:
            match self.criteria:
                case 'average':
                    match len(self.results):
                        case 1:
                            self.currentResult = self.results[0]

                        case 2:
                            self.currentResult = round((self.results[0] + self.results[1]) / 2)

                        case _:
                            self.currentResult = round((sum(self.results) - max(self.results) - min(self.results)) / (len(self.results) - 2))
                case 'mean':
                    self.currentResult = round(sum(self.results) / (len(self.results)))
                case 'single':
                    self.currentResult = min(self.results)

    def showLine(self):
        self.canvas.create_rectangle(0, (self.ranking - 1) * self.height, self.widthName, self.ranking * self.height, fill='#000', outline='')
        self.canvas.create_rectangle(self.widthName, (self.ranking - 1) * self.height, self.widthName + self.widthResults, self.ranking * self.height, fill='#DDD', outline='')

        self.canvas.create_text(self.widthName / 2, (self.ranking - 1) * self.height + self.height / 2, text=self.smallName, fill='#FFF', font=('Helvetica 15 bold'))
        self.canvas.create_text(self.widthName + self.widthResults / 2, (self.ranking - 1) * self.height + self.height / 2, text=utils.getReadableResult(self.currentResult), fill='#000', font=('Helvetica 15 bold'))