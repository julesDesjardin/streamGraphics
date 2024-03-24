import tkinter as tk
from tkinter import ttk
import json
import utils
import TimeTowerLine

class TimeTowerContent:

    def __init__(self, root, queue, widthRanking, widthFlagRectangle, widthFlag, heightFlag, widthName, widthCount, widthResult, fontRanking, fontName, fontCount, fontIncompleteResult, fontResult, height, heightSeparator, maxNumber, reloadDelay):
        self.root = root
        self.frame = tk.Frame(root)
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
        self.height = height
        self.heightSeparator = heightSeparator
        self.canvas = tk.Canvas(self.frame, width = widthRanking + widthFlagRectangle + widthName + widthCount + widthResult, height = maxNumber * (height + heightSeparator), bg='#FFF')
        self.queue = queue
        self.roundId = 0
        self.criteria = ''
        self.lines = []
        self.reloadDelay = reloadDelay
    
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
            self.lines.append(TimeTowerLine.TimeTowerLine(self.canvas, self.widthRanking, self.widthFlagRectangle, self.widthFlag, self.heightFlag, self.widthName, self.widthCount, self.widthResult, self.fontRanking, self.fontName, self.fontCount, self.fontIncompleteResult, self.fontResult, self.height, self.heightSeparator, roundId, person['person']['id'], person['person']['country']['iso2'], person['person']['name'], criteria))

    def updateResults(self):

        while True:
            try:
                (roundId, criteria) = self.queue.get(timeout=0.1)
            except:
                break
            self.updateRound(roundId, criteria)

        if(self.roundId != 0):
            query = f'''
            query MyQuery {{
                round(id: "{self.roundId}") {{
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
        self.root.after(self.reloadDelay, lambda:self.updateResults())

    def showFrame(self):
        self.canvas.pack()
        self.frame.pack(padx = 20, pady = 20)
