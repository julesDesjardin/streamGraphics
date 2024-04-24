import tkinter as tk
from tkinter import ttk
import json
import utils
import TimeTowerLine, constants
import threading, queue, time

class TimeTowerContent:

    def __init__(self, root, queueRound, region, bgLocalName, bgLocalResult, bgForeignerName, bgForeignerResult, widthRanking, widthFlagRectangle, widthFlag, heightFlag, widthName, widthCount, widthResult, fontRanking, fontName, fontCount, fontIncompleteResult, fontResult, colorLocalName, colorLocalResult, colorForeignerName, colorForeignerResult, height, heightSeparator, maxNumber, reloadDelay, roundId, criteria):
        self.root = root
        self.frame = tk.Frame(root)
        self.region = region
        self.bgLocalName = bgLocalName
        self.bgLocalResult = bgLocalResult
        self.bgForeignerName = bgForeignerName
        self.bgForeignerResult = bgForeignerResult
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
        self.fontIncompleteResult  = fontIncompleteResult
        self.fontResult = fontResult
        self.colorLocalName = colorLocalName
        self.colorLocalResult = colorLocalResult
        self.colorForeignerName = colorForeignerName
        self.colorForeignerResult = colorForeignerResult
        self.height = height
        self.heightSeparator = heightSeparator
        self.canvas = tk.Canvas(self.frame, width = widthRanking + widthFlagRectangle + widthName + widthCount + widthResult, height = maxNumber * (height + heightSeparator), bg='#FFF')
        self.queueRound = queueRound
        self.queueRanking = queue.Queue()
        self.roundId = roundId
        self.criteria = criteria
        self.lines = []
        self.reloadDelay = reloadDelay
        self.stop = 0
        self.threadResults = threading.Thread(target=self.resultsLoop)
        self.threadResults.daemon = True
        self.threadResults.start()

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
                country {{
                iso2
                }}
            }}
            }}
        }}
        }}
        '''

        queryResult = utils.getQueryResult(query)
        for person in queryResult['round']['results']:
            if self.region == 'World' or self.region in constants.COUNTRIES[person['person']['country']['iso2']]:
                bgName = self.bgLocalName
                bgResult = self.bgLocalResult
                colorName = self.colorLocalName
                colorResult = self.colorLocalResult
            else:
                bgName = self.bgForeignerName
                bgResult = self.bgForeignerResult
                colorName = self.colorForeignerName
                colorResult = self.colorForeignerResult
            self.lines.append(TimeTowerLine.TimeTowerLine(self.canvas, bgName, bgResult, self.widthRanking, self.widthFlagRectangle, self.widthFlag, self.heightFlag, self.widthName, self.widthCount, self.widthResult, self.fontRanking, self.fontName, self.fontCount, self.fontIncompleteResult, self.fontResult, colorName, colorResult, self.height, self.heightSeparator, roundId, person['person']['id'], person['person']['country']['iso2'], person['person']['name'], criteria))

    def resultsLoop(self):

        while True:
            if(self.roundId != 0):
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

                queryResult = utils.getQueryResult(query)
                self.queueRanking.put(queryResult)
            time.sleep(self.reloadDelay/1000)
            if self.stop == 1:
                break

    def mainLoop(self):

        # Update round
        while True:
            try:
                (roundId, criteria) = self.queueRound.get(timeout=0.1)
            except:
                break
            self.updateRound(roundId, criteria)
        
        # TODO: Expand lines

        # Update results

        while True:
            try:
                queryResult = self.queueRanking.get(timeout=0.1)
            except:
                break

            if int(queryResult['round']['id']) == self.roundId:
                unorderedResults = []
                for line in self.lines:
                    line.updateResults(queryResult)
                    bestResult = utils.DNF_ATTEMPT
                    if len(line.results) > 0:
                        bestResult = min(line.results)
                    unorderedResults.append((line.competitorId, line.currentResult, bestResult))

                orderedResults = sorted(unorderedResults, key=lambda result: (result[1], result[2]))
                for line in self.lines:
                    line.ranking = [result[0] for result in orderedResults].index(line.competitorId) + 1 # +1 because first index is 0

                self.canvas.delete('all')
                for line in self.lines:
                    line.showLine()

        # End of loop, loop again after 1 second
        self.root.after(1000, lambda:self.mainLoop())

    def showFrame(self):
        self.canvas.pack()
        self.frame.pack(padx = 20, pady = 20)
