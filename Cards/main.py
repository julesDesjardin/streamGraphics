import tkinter as tk
from tkinter import ttk
import CardsSettings

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

def checkBothQueues(root, queueLeft, queueRight, canvasLeft, canvasRight, textLeft, textRight):
    checkQueue(root, queueLeft, canvasLeft, textLeft)
    checkQueue(root, queueRight, canvasRight, textRight)

##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Cards')

##############################################################################
# SETTINGS
##############################################################################

localSettings = CardsSettings.CardsSettings(root)
localSettings.showFrame()

##############################################################################
# MAIN
##############################################################################

main = tk.Frame(root)
main.pack()

width = 1000
height = 3000
fontSize = 100

canvasLeft = tk.Canvas(main, width=width, height=height, background='#ff00ff')
canvasRight = tk.Canvas(main, width=width, height=height, background='#ff00ff')
textLeft = canvasLeft.create_text(100, 100, font=f'Helvetica {fontSize}', text='Bonjour', anchor='nw')
textRight = canvasRight.create_text(100, 100, font=f'Helvetica {fontSize}', text='Bonjour', anchor='nw')
canvasLeft.pack(side=tk.LEFT)
canvasRight.pack(side=tk.LEFT)

##############################################################################

checkBothQueues(root, localSettings.queueLeft, localSettings.queueRight, canvasLeft, canvasRight, textLeft, textRight)

root.mainloop()