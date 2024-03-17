import tkinter as tk
from tkinter import ttk
import json
import utils
import TimeTowerLine

class TimeTowerContent:

    def __init__(self, root, queue, widthName, widthResult, height, maxNumber):
        self.root = root
        self.frame = tk.Frame(root)
        self.widthName = widthName
        self.widthResult = widthResult
        self.height = height
        self.canvas = tk.Canvas(self.frame, width=widthName+widthResult, height=maxNumber*height)
        self.queue = queue
        self.roundId = 0
        self.criteria = ''
        self.lines = []
    
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
            self.lines.append(TimeTowerLine.TimeTowerLine(self.canvas, self.widthName, self.widthResult, self.height, roundId, person['person']['id'], person['person']['country']['iso2'], person['person']['name'], criteria))

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
                bestResult = utils.MAX_RESULT
                if len(line.results) > 0:
                    bestResult = min(line.results)
                unorderedResults.append((line.competitorId, line.currentResult, bestResult))

            orderedResults = sorted(unorderedResults, key=lambda result: (result[1], result[2]))
            for line in self.lines:
                line.ranking = [result[0] for result in orderedResults].index(line.competitorId) + 1 # +1 because first index is 0

        self.canvas.delete('all')
        for line in self.lines:
            line.showLine()
        self.root.after(5000, lambda:self.updateResults())

    def showFrame(self):
        self.canvas.pack()
        self.frame.pack()
