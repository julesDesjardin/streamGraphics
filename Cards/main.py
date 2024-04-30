import tkinter as tk
from tkinter import ttk
import CardsSettings

CAMERAS_COUNT = 4

##############################################################################
# FUNCTIONS
##############################################################################


def checkQueue(root, queue, canvas, text):
    while True:
        try:
            data = queue.get(timeout=0.1)
        except:
            break
        canvas.itemconfig(text, text=data)
    root.after(1000, lambda: checkQueue(root, queue, canvas, text))


def checkAllQueues(root, queues, canvases, texts):
    for i in range(0, CAMERAS_COUNT):
        checkQueue(root, queues[i], canvases[i], texts[i])


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

checkAllQueues(root, localSettings.queues, localSettings.canvases, localSettings.texts)

root.mainloop()
