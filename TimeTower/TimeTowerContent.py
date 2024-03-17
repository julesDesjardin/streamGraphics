import tkinter as tk
from tkinter import ttk
import json
import utils
import TimeTowerLine

class TimeTowerContent:

    def __init__(self, root, queue):
        self.root = root
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
            self.lines.append(TimeTowerLine.TimeTowerLine(roundId, person['person']['id'], person['person']['country']['iso2'], person['person']['name'], criteria))

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


        for line in self.lines:
            print(f'{line.fullName} ({line.smallName}) : {line.ranking}')
        self.root.after(5000, lambda:self.updateResults())

