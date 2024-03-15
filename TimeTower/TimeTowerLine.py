import tkinter as tk
from tkinter import ttk
import json
import utils

class TimeTowerLine:

    def __init__(self, roundId, competitorId, country, name):
        self.roundId = roundId
        self.competitorId = competitorId
        self.country = country
        self.fullName = name.split('(')[0].strip() # Removes part in parentheses (could mess up the display, + messes up the 3 letter name) + trailing space in this case
        fullNameSplit = self.fullName.split(' ')
        self.smallName = (fullNameSplit[0][0] + '. ' + fullNameSplit[-1][0:3]).upper()
        self.results = []
        self.currentResult = 0
        self.ranking = 0

