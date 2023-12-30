import tkinter as tk
from tkinter import ttk
import os, threading
import dataRead

LINE_COUNT = 3

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
canvasRight = tk.Canvas(main, width=width, height=totalHeight+5, background='#f9f8eb')
canvasRight.pack(side=tk.LEFT)
lineLeft = canvasLeft.create_rectangle(50, 5, 60, totalHeight, fill='black')
lineRight = canvasRight.create_rectangle(50, 5, 60, totalHeight, fill='black')
textsLeft = []
textsRight = []
for i in range(0,LINE_COUNT):
    textsLeft.append(canvasLeft.create_text(leftLimit, i*lineHeight+lineHeight/2, font='Helvetica 30', text='', anchor='w'))
    textsRight.append(canvasRight.create_text(leftLimit, i*lineHeight+lineHeight/2, font='Helvetica 30', text='', anchor='w'))

stopEvent = threading.Event()
readThreadLeft = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, 0, canvasLeft, textsLeft))
readThreadLeft.start()
readThreadRight = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, 1, canvasRight, textsRight))
readThreadRight.start()

root.protocol("WM_DELETE_WINDOW", lambda:closeWindow(root, stopEvent))
root.mainloop()