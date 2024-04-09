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
    root.after(1000, lambda:checkQueue(root, queue, canvas, text))

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

##############################################################################
# MAIN
##############################################################################

main = tk.Frame(root)
main.pack()

width = 1000
height = 3000
fontSize = 100

canvases = []
texts = []
for i in range(0, CAMERAS_COUNT):
    canvases.append(tk.Canvas(main, width=width, height=height, background='#ff00ff'))
    texts.append(canvases[i].create_text(100, 100, font=f'Helvetica {fontSize}', text=f'Camera {i+1} text', anchor='nw'))
    canvases[i].pack(side=tk.LEFT)

##############################################################################

checkAllQueues(root, localSettings.queues, canvases, texts)

root.mainloop()