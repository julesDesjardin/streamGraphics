import tkinter as tk
from tkinter import ttk

import TimeTowerSettings, TimeTowerContent, utils

timeTower = TimeTowerContent.TimeTowerContent(0, '')

##############################################################################
# FUNCTIONS
##############################################################################

def updateResults(root, queue):
    global timeTower
    while True:
        try:
            (roundId, criteria) = queue.get(timeout=0.1)
        except:
            break
        timeTower = TimeTowerContent.TimeTowerContent(roundId, criteria)

    if(timeTower.roundId != 0):
        timeTower.updateResults()
        for line in timeTower.lines:
            print(f'{line.fullName} ({line.smallName}) : {line.ranking}')

    root.after(5000, lambda:updateResults(root, queue))

##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Time Tower')

##############################################################################
# SETTINGS
##############################################################################

localSettings = TimeTowerSettings.TimeTowerSettings(root)
localSettings.showFrame()

##############################################################################

updateResults(root, localSettings.queue)
root.mainloop()