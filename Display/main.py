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
lineHeight = 100
totalHeight = 3*lineHeight

canvasLeft = tk.Canvas(main, width=width, height=totalHeight+5, background='#f9f8eb')
canvasLeft.pack(side=tk.LEFT)
lineLeft = canvasLeft.create_rectangle(50, 5, 60, totalHeight, fill='black')
nameTextLeft = canvasLeft.create_text(leftLimit, lineHeight/2, font='Helvetica 30', text = '', anchor='w')
singleTextLeft = canvasLeft.create_text(leftLimit, lineHeight+lineHeight/2, font='Helvetica 30', text= 'PR Single', anchor='w')
averageTextLeft = canvasLeft.create_text(leftLimit, 2*lineHeight+lineHeight/2, font='Helvetica 30', text= 'PR Average', anchor='w')
canvasRight = tk.Canvas(main, width=width, height=totalHeight+5, background='#f9f8eb')
canvasRight.pack(side=tk.LEFT)
lineRight = canvasRight.create_rectangle(50, 5, 60, totalHeight, fill='black')
nameTextRight = canvasRight.create_text(leftLimit, lineHeight/2, font='Helvetica 30', text = '', anchor='w')
singleTextRight = canvasRight.create_text(leftLimit, lineHeight+lineHeight/2, font='Helvetica 30', text= 'PR Single', anchor='w')
averageTextRight = canvasRight.create_text(leftLimit, 2*lineHeight+lineHeight/2, font='Helvetica 30', text= 'PR Average', anchor='w')

stopEvent = threading.Event()
readThreadLeft = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, 0, canvasLeft, nameTextLeft, singleTextLeft, averageTextLeft))
readThreadLeft.start()
readThreadRight = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, 1, canvasRight, nameTextRight, singleTextRight, averageTextRight))
readThreadRight.start()

root.protocol("WM_DELETE_WINDOW", lambda:closeWindow(root, stopEvent))
root.mainloop()