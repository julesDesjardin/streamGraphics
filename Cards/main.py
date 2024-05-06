import tkinter as tk
from tkinter import ttk
import time
import queue
import CardsSettings
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import Flag

CAMERAS_X = 2
CAMERAS_Y = 2
CAMERAS_COUNT = CAMERAS_X * CAMERAS_Y

##############################################################################
# FUNCTIONS
##############################################################################


def checkQueue(root, dataQueue, canvas, text, flag, flagImage, background, backgroundLoopIndex):
    try:
        (country, data) = dataQueue.get(block=False)
        if data == '':
            canvas.itemconfig(background, state='hidden')
            canvas.itemconfig(flagImage, state='hidden')
            canvas.itemconfig(text, state='hidden')
            backgroundLoopIndex = -1
        else:
            if backgroundLoopIndex == -1:
                if localSettings.introFile != '':
                    for image in localSettings.introImages:
                        canvas.itemconfig(background, image=image, state='normal')
                        canvas.update()
                        time.sleep(1 / 25)
                backgroundLoopIndex = 0
            flag = Flag.getFlag(localSettings.flagWidth, localSettings.flagHeight, country)
            canvas.itemconfig(flagImage, image=flag, state='normal')
            canvas.itemconfig(text, text=data, state='normal')
    except queue.Empty:
        pass
    if backgroundLoopIndex != -1:
        canvas.itemconfig(background, image=localSettings.loopImages[backgroundLoopIndex], state='normal')
        canvas.update()
        if backgroundLoopIndex == len(localSettings.loopImages) - 1:
            backgroundLoopIndex = 0
        else:
            backgroundLoopIndex = backgroundLoopIndex + 1
    root.after(int(1000 / 25), lambda: checkQueue(root, dataQueue, canvas, text, flag, flagImage, background, backgroundLoopIndex))


def checkAllQueues(root, queues, canvases, texts, flags, flagImages, backgrounds):
    for i in range(0, CAMERAS_COUNT):
        checkQueue(root, queues[i], canvases[i], texts[i], flags[i], flagImages[i], backgrounds[i], -1)


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

##############################################################################

checkAllQueues(root, localSettings.queues, localSettings.canvases, localSettings.texts,
               localSettings.flags, localSettings.flagImages, localSettings.backgrounds)

root.mainloop()
