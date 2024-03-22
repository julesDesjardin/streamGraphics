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

timeTower = TimeTowerContent.TimeTowerContent(root, localSettings.queue, 50, 60, 45, 30, 100, 50, 100, 'Helvetica 15 bold', 'Helvetica 15 bold', 'Helvetica 15', 'Helvetica 12 italic', 'Helvetica 15 bold', 50, 10, 16)
timeTower.updateResults()
timeTower.showFrame()

root.mainloop()