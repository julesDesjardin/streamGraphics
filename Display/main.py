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

canvas = tk.Canvas(main, width=width, height=totalHeight+5, background='magenta')
line = canvas.create_rectangle(50, 5, 60, totalHeight, fill='black')
nameText = canvas.create_text(leftLimit, lineHeight/2, text = '', anchor='w')
singleText = canvas.create_text(leftLimit, lineHeight+lineHeight/2, text= 'PR Single', anchor='w')
averageText = canvas.create_text(leftLimit, 2*lineHeight+lineHeight/2, text= 'PR Average', anchor='w')
canvas.pack()

stopEvent = threading.Event()
readThread = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(stopEvent, canvas, nameText, singleText, averageText))
readThread.start()

root.protocol("WM_DELETE_WINDOW", lambda:closeWindow(root, stopEvent))
root.mainloop()