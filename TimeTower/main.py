import tkinter as tk
from tkinter import ttk

import TimeTowerSettings, TimeTowerContent, utils

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

# root.mainloop()
localSettings.compId = 2865
localSettings.roundId = 40414

test = TimeTowerContent.TimeTowerContent(localSettings.roundId, 'average')
test.updateResults()

for line in test.lines:
    print(f'{line.fullName} ({line.smallName}) : {line.ranking}')