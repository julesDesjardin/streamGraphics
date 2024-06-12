import tkinter as tk
from tkinter import ttk
import time
import queue
import CardsSettings
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import Image

CAMERAS_X = 2
CAMERAS_Y = 2
CAMERAS_COUNT = CAMERAS_X * CAMERAS_Y

##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Cards')

##############################################################################
# SETTINGS
##############################################################################

localSettings = CardsSettings.CardsSettings(root, CAMERAS_X, CAMERAS_Y)
localSettings.showFrame()
localSettings.mainFrame.pack()
localSettings.checkAllQueues()

##############################################################################

root.mainloop()
