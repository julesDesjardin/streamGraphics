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

timeTower = TimeTowerContent.TimeTowerContent(root, localSettings.queue)
timeTower.updateResults()

root.mainloop()