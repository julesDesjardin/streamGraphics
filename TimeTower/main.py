import tkinter as tk
from tkinter import ttk

import TimeTowerSettings, utils

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

root.mainloop()