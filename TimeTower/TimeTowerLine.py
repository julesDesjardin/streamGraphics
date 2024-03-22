import tkinter as tk
from tkinter import ttk
import os
import utils
from urllib.request import urlopen

class TimeTowerLine:

    def __init__(self, canvas, widthFlag, widthName, widthCount, widthResult, fontName, fontCount, fontIncompleteResult, fontResult, height, roundId, competitorId, country, name, criteria):
        self.canvas = canvas
        self.flagImage = None
        self.widthFlag = widthFlag
        self.widthName = widthName
        self.widthCount = widthCount
        self.widthResult = widthResult
        self.fontName = fontName
        self.fontCount = fontCount
        self.fontIncompleteResult = fontIncompleteResult
        self.fontResult = fontResult
        self.height = height
        self.roundId = roundId
        self.competitorId = competitorId
        self.country = country
        self.fullName = name.split('(')[0].strip() # Removes part in parentheses (could mess up the display, + messes up the 3 letter name) + trailing space in this case
        fullNameSplit = self.fullName.split(' ')
        self.smallName = (fullNameSplit[0][0] + '. ' + fullNameSplit[-1][0:3]).upper()
        self.criteria = criteria
        if criteria == 'average':
            self.maxResults = 5
        else:
            self.maxResults = 3
        self.results = []
        self.currentResult = 0
        self.ranking = 0

    def updateResults(self, queryResult):
        for result in queryResult['round']['results']:
            if result['person']['id'] == self.competitorId:
                self.results = []
                for attempt in result['attempts']:
                    if attempt['result'] < 0:
                        nonDNFResult = utils.DNF_ATTEMPT
                    else:
                        nonDNFResult = attempt['result']
                    self.results.append(nonDNFResult)
        
        # Update currentResult
        if len(self.results) == 0:
            self.currentResult = utils.DNF_ATTEMPT
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
        # Empty rectangles
        self.canvas.create_rectangle(0, (self.ranking - 1) * self.height, self.widthFlag + self.widthName, self.ranking * self.height, fill='#000', outline='')
        self.canvas.create_rectangle(self.widthFlag + self.widthName, (self.ranking - 1) * self.height, self.widthName + self.widthName + self.widthCount + self.widthResult, self.ranking * self.height, fill='#DDD', outline='')

        # Flag
        if utils.DEBUG_MODE_LOCAL_FLAG:
            flagImageFull = tk.PhotoImage(file=f'{os.path.dirname(__file__)}/us.png')
        else:
            image_url = f'https://flagcdn.com/w320/{self.country.lower()}.png'
            image_byt = urlopen(image_url).read()
            flagImageFull = tk.PhotoImage(data=image_byt)
        flagFullWidth = flagImageFull.width()
        flagFullHeight = flagImageFull.height()
        self.flagImage = flagImageFull.zoom(self.widthFlag, self.height).subsample(flagFullWidth, flagFullHeight) # Resize
        self.canvas.create_image(self.widthFlag / 2, (self.ranking - 1) * self.height + self.height / 2, image=self.flagImage)

        # Name
        self.canvas.create_text(self.widthFlag + self.widthName / 2, (self.ranking - 1) * self.height + self.height / 2, text=self.smallName, fill='#FFF', font=(self.fontName))
        # Count
        self.canvas.create_text(self.widthFlag + self.widthName + self.widthCount / 2, (self.ranking - 1) * self.height + self.height / 2, text=f'({len(self.results)}/{self.maxResults})', fill='#000', font=(self.fontCount))
        # Result
        if len(self.results) == self.maxResults:
            fontResult = self.fontResult
        else:
            fontResult = self.fontIncompleteResult
        self.canvas.create_text(self.widthFlag + self.widthName + self.widthCount + self.widthResult / 2, (self.ranking - 1) * self.height + self.height / 2, text=utils.getReadableResult(self.currentResult), fill='#000', font=(fontResult))
