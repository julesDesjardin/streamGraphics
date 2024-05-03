import tkinter as tk
from tkinter import ttk
import CardsSettings
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import Flag

CAMERAS_COUNT = 4

##############################################################################
# FUNCTIONS
##############################################################################


def checkQueue(root, queue, canvas, text, flag, flagImage):
    while True:
        try:
            (country, data) = queue.get(timeout=0.1)
        except:
            break
        flag = Flag.getFlag(localSettings.flagWidth, localSettings.flagHeight, country)
        canvas.itemconfig(flagImage, image=flag)
        canvas.itemconfig(text, text=data)
    root.after(1000, lambda: checkQueue(root, queue, canvas, text, flag, flagImage))


def checkAllQueues(root, queues, canvases, texts, flags, flagImages):
    for i in range(0, CAMERAS_COUNT):
        checkQueue(root, queues[i], canvases[i], texts[i], flags[i], flagImages[i])


##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Cards')

##############################################################################
# SETTINGS
##############################################################################

localSettings = CardsSettings.CardsSettings(root, CAMERAS_COUNT)
localSettings.showFrame()
localSettings.mainFrame.pack()

##############################################################################

checkAllQueues(root, localSettings.queues, localSettings.canvases, localSettings.texts, localSettings.flags, localSettings.flagImages)

root.mainloop()
