import tkinter as tk
from tkinter import ttk
import os
import utils
from urllib.request import urlopen

class TimeTowerLine:

    def __init__(self, canvas, widthRanking, widthFlagRectangle, widthFlag, heightFlag, widthName, widthCount, widthResult, fontRanking, fontName, fontCount, fontIncompleteResult, fontResult, height, heightSeparator, roundId, competitorId, country, name, criteria):
        self.canvas = canvas
        self.flagImage = None
        self.widthRanking = widthRanking
        self.widthFlagRectangle = widthFlagRectangle
        self.widthFlag = widthFlag
        self.heightFlag = heightFlag
        self.widthName = widthName
        self.widthCount = widthCount
        self.widthResult = widthResult
        self.fontRanking = fontRanking
        self.fontName = fontName
        self.fontCount = fontCount
        self.fontIncompleteResult = fontIncompleteResult
        self.fontResult = fontResult
        self.height = height
        self.heightSeparator = heightSeparator
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
        currentX = 0
        currentY = (self.ranking - 1) * (self.height + self.heightSeparator)
        
        # Ranking
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthRanking, currentY + self.height, fill='#000', outline='')
        self.canvas.create_text(currentX + self.widthRanking / 2, currentY + self.height / 2, text=self.ranking, fill='#FFF', font=(self.fontRanking))
        currentX = currentX + self.widthRanking

        # Flag
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthFlagRectangle, currentY + self.height, fill='#000', outline='')
        if utils.DEBUG_MODE_LOCAL_FLAG:
            flagImageFull = tk.PhotoImage(file=f'{os.path.dirname(__file__)}/us.png')
        else:
            image_url = f'https://flagcdn.com/w320/{self.country.lower()}.png'
            image_byt = urlopen(image_url).read()
            flagImageFull = tk.PhotoImage(data=image_byt)
        flagFullWidth = flagImageFull.width()
        flagFullHeight = flagImageFull.height()
        self.flagImage = flagImageFull.zoom(self.widthFlag, self.heightFlag).subsample(flagFullWidth, flagFullHeight) # Resize
        self.canvas.create_image(currentX + self.widthFlagRectangle / 2, currentY + self.height / 2, image=self.flagImage)
        currentX = currentX + self.widthFlagRectangle

        # Name
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthName, currentY + self.height, fill='#000', outline='')
        self.canvas.create_text(currentX + self.widthName / 2, currentY + self.height / 2, text=self.smallName, fill='#FFF', font=(self.fontName))
        currentX = currentX + self.widthName

        # Count
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthCount, currentY + self.height, fill='#AAA', outline='')
        self.canvas.create_text(currentX + self.widthCount / 2, currentY + self.height / 2, text=f'({len(self.results)}/{self.maxResults})', fill='#000', font=(self.fontCount))
        currentX = currentX + self.widthCount

        # Result
        if len(self.results) == self.maxResults:
            fontResult = self.fontResult
        else:
            fontResult = self.fontIncompleteResult
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthResult, currentY + self.height, fill='#AAA', outline='')
        self.canvas.create_text(currentX + self.widthResult / 2, currentY + self.height / 2, text=utils.getReadableResult(self.currentResult), fill='#000', font=(fontResult))
        currentX = currentX + self.widthResult
