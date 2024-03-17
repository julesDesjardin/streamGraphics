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

timeTower = TimeTowerContent.TimeTowerContent(root, localSettings.queue, 150, 50, 50, 16)
timeTower.updateResults()
timeTower.showFrame()

root.mainloop()