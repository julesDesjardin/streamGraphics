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
# FUNCTIONS
##############################################################################


def checkQueue(root, dataQueue, canvas, name, text, flag, flagImage, avatar, avatarImage, background, backgroundLoopIndex):
    try:
        (country, nameRead, avatarRead, textRead) = dataQueue.get(block=False)
        if nameRead == '':
            canvas.itemconfig(background, state='hidden')
            canvas.itemconfig(flagImage, state='hidden')
            canvas.itemconfig(avatarImage, state='hidden')
            canvas.itemconfig(name, state='hidden')
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
            flag = Image.getFlag(localSettings.flagHeight, country)
            canvas.itemconfig(flagImage, image=flag, state='normal')
            avatar = Image.getAvatar(localSettings.avatarWidth, localSettings.avatarHeight, avatarRead)
            canvas.itemconfig(avatarImage, image=avatar, state='normal')
            canvas.itemconfig(name, text=nameRead, state='normal')
            canvas.itemconfig(text, text=textRead, state='normal')
    except queue.Empty:
        pass
    if backgroundLoopIndex != -1:
        canvas.itemconfig(background, image=localSettings.loopImages[backgroundLoopIndex], state='normal')
        canvas.update()
        if backgroundLoopIndex == len(localSettings.loopImages) - 1:
            backgroundLoopIndex = 0
        else:
            backgroundLoopIndex = backgroundLoopIndex + 1
    root.after(int(1000 / 25), lambda: checkQueue(root, dataQueue, canvas, name, text,
               flag, flagImage, avatar, avatarImage, background, backgroundLoopIndex))


def checkAllQueues(root, queues, canvases, names, texts, flags, flagImages, avatars, avatarImages, backgrounds):
    for i in range(0, CAMERAS_COUNT):
        checkQueue(root, queues[i], canvases[i], names[i], texts[i], flags[i], flagImages[i], avatars[i], avatarImages[i], backgrounds[i], -1)


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

checkAllQueues(root, localSettings.queues, localSettings.canvases, localSettings.names, localSettings.texts,
               localSettings.flags, localSettings.flagImages, localSettings.avatars, localSettings.avatarImages, localSettings.backgrounds)

root.mainloop()
