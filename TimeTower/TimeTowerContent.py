import tkinter as tk
from tkinter import ttk
import json
import utils
import TimeTowerLine

class TimeTowerContent:

    def __init__(self, roundId):
        self.roundId = roundId
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

        result = utils.getQueryResult(query)
        for person in result['round']['results']:
            self.lines.append(TimeTowerLine.TimeTowerLine(roundId, person['person']['id'], person['person']['country']['iso2'], person['person']['name']))

