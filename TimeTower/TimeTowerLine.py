import tkinter as tk
from tkinter import ttk
import utils
from urllib.request import urlopen


import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import Flag


class TimeTowerLine:

    def __init__(self, canvas, bgName, bgResult, widthRanking, widthFlagRectangle, heightFlag, widthName, widthFullName, widthCount, widthResult, widthFullResult, fontRanking, fontName, fontCount, fontIncompleteResult, fontResult, fontFullResult, colorName, colorResult, height, heightSeparator, roundId, competitorId, competitorRegistrantId, country, name, criteria, stepXmax, stepYmax):
        self.canvas = canvas
        self.bgName = bgName
        self.bgResult = bgResult
        self.flagImage = None
        self.widthRanking = widthRanking
        self.widthFlagRectangle = widthFlagRectangle
        self.heightFlag = heightFlag
        self.widthName = widthName
        self.widthFullName = widthFullName
        self.widthCount = widthCount
        self.widthResult = widthResult
        self.widthFullResult = widthFullResult
        self.fontRanking = fontRanking
        self.fontName = fontName
        self.fontCount = fontCount
        self.fontIncompleteResult = fontIncompleteResult
        self.fontResult = fontResult
        self.fontFullResult = fontFullResult
        self.colorName = colorName
        self.colorResult = colorResult
        self.height = height
        self.heightSeparator = heightSeparator
        self.roundId = roundId
        self.competitorId = competitorId
        self.competitorRegistrantId = competitorRegistrantId
        self.country = country
        # Removes part in parentheses (could mess up the display, + messes up the 3 letter name) + trailing space in this case
        self.fullName = name.split('(')[0].strip().upper()
        fullNameSplit = self.fullName.split(' ')
        self.smallName = (fullNameSplit[0][0] + '. ' + fullNameSplit[-1][0:3])
        self.criteria = criteria
        if criteria == 'average':
            self.maxResults = 5
        else:
            self.maxResults = 3
        self.results = []
        self.currentResult = 0
        self.ranking = 0
        self.nextRanking = 0
        self.expanded = False
        self.expandRequest = False
        self.reduceRequest = False
        self.stepXmax = stepXmax
        self.stepYmax = stepYmax
        if utils.DEBUG_MODE_LOCAL_FLAG:
            country = 'local'
        else:
            country = self.country
        self.flagImage = Flag.getFlag(self.heightFlag, country)

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

    def showLine(self, stepX, stepY):
        currentX = 0
        currentRanking = self.ranking + (self.nextRanking - self.ranking) * (stepY / self.stepYmax)
        currentY = int((currentRanking - 1) * (self.height + self.heightSeparator))

        # Ranking
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthRanking, currentY + self.height, fill=self.bgName, outline='')
        self.canvas.create_text(currentX + self.widthRanking / 2, currentY + self.height / 2,
                                text=self.nextRanking, fill=self.colorName, font=(self.fontRanking))
        currentX = currentX + self.widthRanking

        # Flag
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthFlagRectangle, currentY + self.height, fill=self.bgName, outline='')
        self.canvas.create_image(currentX + self.widthFlagRectangle / 2, currentY + self.height / 2, image=self.flagImage)
        currentX = currentX + self.widthFlagRectangle

        # Name
        if self.expandRequest:
            currentWidthName = self.widthName + int((self.widthFullName - self.widthName) * (stepX / self.stepXmax))
            self.canvas.create_rectangle(currentX, currentY, currentX + currentWidthName, currentY + self.height, fill=self.bgName, outline='')
            self.canvas.create_text(currentX, currentY + self.height / 2, text=self.fullName, fill=self.colorName, font=(self.fontName), anchor='w')
            currentX = currentX + currentWidthName
        elif self.reduceRequest:
            currentWidthName = self.widthFullName - int((self.widthFullName - self.widthName) * (stepX / self.stepXmax))
            self.canvas.create_rectangle(currentX, currentY, currentX + currentWidthName, currentY + self.height, fill=self.bgName, outline='')
            self.canvas.create_text(currentX, currentY + self.height / 2, text=self.smallName, fill=self.colorName, font=(self.fontName), anchor='w')
            currentX = currentX + currentWidthName
        elif self.expanded:
            self.canvas.create_rectangle(currentX, currentY, currentX + self.widthFullName, currentY + self.height, fill=self.bgName, outline='')
            self.canvas.create_text(currentX, currentY + self.height / 2, text=self.fullName, fill=self.colorName, font=(self.fontName), anchor='w')
            currentX = currentX + self.widthFullName
        else:
            self.canvas.create_rectangle(currentX, currentY, currentX + self.widthName, currentY + self.height, fill=self.bgName, outline='')
            self.canvas.create_text(currentX, currentY + self.height / 2, text=self.smallName, fill=self.colorName, font=(self.fontName), anchor='w')
            currentX = currentX + self.widthName

        # Count
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthCount, currentY + self.height, fill=self.bgResult, outline='')
        self.canvas.create_text(currentX + self.widthCount / 2, currentY + self.height / 2,
                                text=f'({len(self.results)}/{self.maxResults})', fill=self.colorResult, font=(self.fontCount))
        currentX = currentX + self.widthCount

        # Result
        if len(self.results) == self.maxResults:
            fontResult = self.fontResult
        else:
            fontResult = self.fontIncompleteResult
        self.canvas.create_rectangle(currentX, currentY, currentX + self.widthResult, currentY + self.height, fill=self.bgResult, outline='')
        self.canvas.create_text(currentX + self.widthResult / 2, currentY + self.height / 2,
                                text=utils.getReadableResult(self.currentResult), fill=self.colorResult, font=(fontResult))
        currentX = currentX + self.widthResult

        # Full result
        if self.expandRequest:
            currentWidthFullResult = int(self.widthFullResult * (stepX / self.stepXmax))
            self.canvas.create_rectangle(currentX, currentY, currentX + currentWidthFullResult,
                                         currentY + self.height, fill=self.bgResult, outline='')
            self.canvas.create_text(currentX, currentY + self.height / 2, text=utils.getAllResults(self.results,
                                    self.criteria), fill=self.colorResult, font=(self.fontFullResult), anchor='w')
            currentX = currentX + currentWidthFullResult
        elif self.reduceRequest:
            currentWidthFullResult = int(self.widthFullResult * ((self.stepXmax - stepX) / self.stepXmax))
            self.canvas.create_rectangle(currentX, currentY, currentX + currentWidthFullResult,
                                         currentY + self.height, fill=self.bgResult, outline='')
            currentX = currentX + currentWidthFullResult
        elif self.expanded:
            self.canvas.create_rectangle(currentX, currentY, currentX + self.widthFullResult, currentY + self.height, fill=self.bgResult, outline='')
            self.canvas.create_text(currentX, currentY + self.height / 2, text=utils.getAllResults(self.results,
                                    self.criteria), fill=self.colorResult, font=(self.fontFullResult), anchor='w')
            currentX = currentX + self.widthFullResult
