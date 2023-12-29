import tkinter as tk
from tkinter import ttk
import os, threading
import dataRead

root = tk.Tk()
root.title('Stream Display')

def changePending():
    files = os.listdir('.')
    return 'changePending.txt' in files

def closeWindow(window, event):
    event.set()
    window.destroy()

main = tk.Frame(root)
main.pack()

width = 500
leftLimit = 80
lineHeight = 30
totalHeight = 3*lineHeight

canvasLeft = tk.Canvas(main, width=width, height=totalHeight+5, background='magenta')
line = canvasLeft.create_rectangle(50, 5, 60, totalHeight, fill='black')
nameText = canvasLeft.create_text(leftLimit, lineHeight/2, text = '', anchor='w')
singleText = canvasLeft.create_text(leftLimit, lineHeight+lineHeight/2, text= 'PR Single', anchor='w')
averageText = canvasLeft.create_text(leftLimit, 2*lineHeight+lineHeight/2, text= 'PR Average', anchor='w')
canvasLeft.pack(side=tk.LEFT)
canvasRight = tk.Canvas(main, width=width, height=totalHeight+5, background='magenta')
line = canvasRight.create_rectangle(50, 5, 60, totalHeight, fill='black')
nameText = canvasRight.create_text(leftLimit, lineHeight/2, text = '', anchor='w')
singleText = canvasRight.create_text(leftLimit, lineHeight+lineHeight/2, text= 'PR Single', anchor='w')
averageText = canvasRight.create_text(leftLimit, 2*lineHeight+lineHeight/2, text= 'PR Average', anchor='w')
canvasRight.pack(side=tk.LEFT)

stopEvent = threading.Event()
readThreadLeft = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, 0, canvasLeft, nameText, singleText, averageText))
readThreadLeft.start()
readThreadRight = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, 1, canvasRight, nameText, singleText, averageText))
readThreadRight.start()

root.protocol("WM_DELETE_WINDOW", lambda:closeWindow(root, stopEvent))
root.mainloop()