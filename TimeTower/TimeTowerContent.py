from Common import Image
from Common.commonUtils import COUNTRIES
import tkinter as tk
from tkinter import ttk
import json
import timeTowerUtils
import TimeTowerLine
import threading
import queue
import time

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')


class TimeTowerContent:

    def __init__(self, root, queueRound, queueUpdate, region, nameIsFull, backgroundColor, bgLocalName, bgLocalResult, bgForeignerName, bgForeignerResult, widthRanking, widthFlagRectangle, heightFlag, widthName, widthCount, widthResult, widthBPAWPA, widthBPAWPASeparator, fontRanking, fontName, fontCount, fontIncompleteResult, fontResult, fontBPAWPA, colorLocalName, colorLocalResult, colorForeignerName, colorForeignerResult, height, heightSeparator, maxNumber, reloadDelay, stepXmax, stepYmax, FPS):
        self.root = root
        self.frame = tk.Frame(root)
        self.region = region
        self.nameIsFull = nameIsFull
        self.backgroundColor = backgroundColor
        self.bgLocalName = bgLocalName
        self.bgLocalResult = bgLocalResult
        self.bgForeignerName = bgForeignerName
        self.bgForeignerResult = bgForeignerResult
        self.widthRanking = widthRanking
        self.widthFlagRectangle = widthFlagRectangle
        self.heightFlag = heightFlag
        self.widthName = widthName
        self.widthCount = widthCount
        self.widthResult = widthResult
        self.widthBPAWPA = widthBPAWPA
        self.widthBPAWPASeparator = widthBPAWPASeparator
        self.fontRanking = fontRanking
        self.fontName = fontName
        self.fontCount = fontCount
        self.fontIncompleteResult = fontIncompleteResult
        self.fontResult = fontResult
        self.fontBPAWPA = fontBPAWPA
        self.colorLocalName = colorLocalName
        self.colorLocalResult = colorLocalResult
        self.colorForeignerName = colorForeignerName
        self.colorForeignerResult = colorForeignerResult
        self.height = height
        self.heightSeparator = heightSeparator
        self.canvas = tk.Canvas(self.frame, width=widthRanking + widthFlagRectangle + widthName + widthCount +
                                widthResult + 2*widthBPAWPA + widthBPAWPASeparator, height=maxNumber * (height + heightSeparator), bg=self.backgroundColor)
        self.queueRound = queueRound
        self.queueUpdate = queueUpdate
        self.queueRanking = queue.Queue()
        self.roundId = 0
        self.criteria = ''
        self.lines = []
        self.reloadDelay = reloadDelay
        self.stop = 0
        self.threadResults = threading.Thread(target=self.resultsLoop)
        self.threadResults.daemon = True
        self.threadResults.start()
        self.stepXmax = stepXmax
        self.stepYmax = stepYmax
        self.FPS = FPS
        self.state = timeTowerUtils.TimeTowerState.IDLE
        self.stepXRequest = False
        self.stepYRequest = False
        self.step = 0

    def updateRound(self, roundId, criteria):
        self.roundId = roundId
        self.criteria = criteria
        self.lines = []
        query = f'''
        query MyQuery {{
        round(id: "{roundId}") {{
            results {{
            person {{
                name
                id
                registrantId
                country {{
                iso2
                }}
            }}
            }}
        }}
        }}
        '''

        queryResult = timeTowerUtils.getQueryResult(query)
        for person in queryResult['round']['results']:
            if self.region == 'World' or self.region in COUNTRIES[person['person']['country']['iso2']]:
                bgName = self.bgLocalName
                bgResult = self.bgLocalResult
                colorName = self.colorLocalName
                colorResult = self.colorLocalResult
            else:
                bgName = self.bgForeignerName
                bgResult = self.bgForeignerResult
                colorName = self.colorForeignerName
                colorResult = self.colorForeignerResult
            self.lines.append(TimeTowerLine.TimeTowerLine(self.canvas, bgName, bgResult, self.widthRanking, self.widthFlagRectangle, self.heightFlag, self.widthName, self.widthCount, self.widthResult, self.widthBPAWPA, self.widthBPAWPASeparator, self.fontRanking, self.fontName, self.fontCount,
                              self.fontIncompleteResult, self.fontResult, self.fontBPAWPA, colorName, colorResult, self.height, self.heightSeparator, roundId, person['person']['id'], person['person']['registrantId'], person['person']['country']['iso2'], person['person']['name'], self.nameIsFull, criteria, self.stepXmax, self.stepYmax))

    def resultsLoop(self):

        while True:
            if (self.roundId != 0):
                query = f'''
                query MyQuery {{
                    round(id: "{self.roundId}") {{
                        id
                        results {{
                            person {{
                                id
                            }}
                            attempts {{
                                result
                            }}
                        }}
                    }}
                }}
                '''

                queryResult = timeTowerUtils.getQueryResult(query)
                self.queueRanking.put(queryResult)
            time.sleep(self.reloadDelay / 1000)

    def mainLoop(self):
        start = time.time()
        nextState = self.state
        nextStep = self.step

        match self.state:
            case timeTowerUtils.TimeTowerState.IDLE:

                # Update layout
                try:
                    (self.region,
                     self.widthRanking, self.widthFlagRectangle, self.heightFlag, self.widthName, self.widthCount, self.widthResult, self.widthBPAWPA, self.widthBPAWPASeparator,
                     self.fontRanking, self.fontName, self.fontCount, self.fontIncompleteResult, self.fontResult, self.fontBPAWPA,
                     self.height, self.heightSeparator,
                     self.backgroundColor,
                     self.bgLocalName, self.bgLocalResult,
                     self.bgForeignerName, self.bgForeignerResult,
                     self.colorLocalName, self.colorLocalResult,
                     self.colorForeignerName, self.colorForeignerResult,
                     self.maxNumber, self.reloadDelay, self.stepXmax, self.stepYmax, self.FPS
                     ) = self.queueUpdate.get(block=False)
                    self.canvas.configure(width=self.widthRanking + self.widthFlagRectangle + self.widthCount + self.widthResult + 2*self.widthBPAWPA + self.widthBPAWPASeparator,
                                          height=self.maxNumber * (self.height + self.heightSeparator), bg=self.backgroundColor)
                    for line in self.lines:
                        line.widthRanking = self.widthRanking
                        line.widthFlagRectangle = self.widthFlagRectangle
                        line.heightFlag = self.heightFlag
                        line.flagImage = Image.getFlag(
                            self.heightFlag, line.country)
                        line.widthName = self.widthName
                        line.widthCount = self.widthCount
                        line.widthResult = self.widthResult
                        line.widthBPAWPA = self.widthBPAWPA
                        line.widthBPAWPASeparator = self.widthBPAWPASeparator
                        line.height = self.height
                        line.heightSeparator = self.heightSeparator
                        line.fontRanking = self.fontRanking
                        line.fontName = self.fontName
                        line.fontCount = self.fontCount
                        line.fontIncompleteResult = self.fontIncompleteResult
                        line.fontResult = self.fontResult
                        line.fontBPAWPA = self.fontBPAWPA
                        line.stepXmax = self.stepXmax
                        line.stepYmax = self.stepYmax
                except:
                    pass

                # Update round
                try:
                    (roundId, criteria) = self.queueRound.get(block=False)
                    self.updateRound(roundId, criteria)
                except:
                    pass

                # Update stepX
                self.stepXRequest = False
                for line in self.lines:
                    if line.expandRequest or line.reduceRequest:
                        self.stepXRequest = True

                # Update stepY
                self.stepYRequest = False
                try:
                    queryResult = self.queueRanking.get(block=False)

                    if int(queryResult['round']['id']) == self.roundId:
                        unorderedResults = []
                        for line in self.lines:
                            line.updateResults(queryResult)
                            bestResult = timeTowerUtils.DNF_ATTEMPT
                            if len(line.results) > 0:
                                bestResult = min(line.results)
                            unorderedResults.append((line.competitorId, line.currentResult, bestResult))

                        orderedResults = sorted(unorderedResults, key=lambda result: (result[1], result[2]))
                        for line in self.lines:
                            line.nextRanking = [result[0] for result in orderedResults].index(line.competitorId) + 1  # +1 because first index is 0
                    self.stepYRequest = True
                except:
                    pass

                if self.stepXRequest:
                    self.stepXRequest = False
                    nextState = timeTowerUtils.TimeTowerState.STEP_X
                    nextStep = 0
                elif self.stepYRequest:
                    self.stepYRequest = False
                    nextState = timeTowerUtils.TimeTowerState.STEP_Y
                    nextStep = 0

            case timeTowerUtils.TimeTowerState.STEP_X:
                self.canvas.delete('all')
                for line in self.lines:
                    line.showLine(self.step, 0)
                self.canvas.update()
                if self.step == self.stepXmax:
                    # Expand requests are over, expanded values must be changed
                    for line in self.lines:
                        if line.expandRequest:
                            line.expanded = True
                            line.expandRequest = False
                        if line.reduceRequest:
                            line.expanded = False
                            line.reduceRequest = False

                    if self.stepYRequest:
                        self.stepYRequest = False
                        nextState = timeTowerUtils.TimeTowerState.STEP_Y
                    else:
                        nextState = timeTowerUtils.TimeTowerState.IDLE
                    nextStep = 0
                else:
                    nextStep = self.step + 1

            case timeTowerUtils.TimeTowerState.STEP_Y:
                self.canvas.delete('all')
                for line in self.lines:
                    line.showLine(0, self.step)
                self.canvas.update()
                if self.step == self.stepYmax:
                    nextState = timeTowerUtils.TimeTowerState.IDLE
                    nextStep = 0
                    for line in self.lines:
                        line.ranking = line.nextRanking
                else:
                    nextStep = self.step + 1

        self.state = nextState
        self.step = nextStep
        delay = max(0, int(1000 / self.FPS - 1000 * (time.time() - start)))
        self.root.after(delay, self.mainLoop)

    def showFrame(self):
        self.canvas.pack()
        self.frame.pack(padx=20, pady=20, side=tk.RIGHT)
