import tkinter as tk
from tkinter import ttk
import os, threading
import dataRead

root = tk.Tk()

def changePending():
    files = os.listdir('.')
    return 'changePending.txt' in files

main = tk.Frame(root)
main.pack()

width = 500
lineHeight = 200
totalHeight = 3*lineHeight

canvas = tk.Canvas(main, width=width, height=totalHeight, background='magenta')
nameText = canvas.create_text(width/2, lineHeight/2, text = '', anchor="center", justify='center')
singleText = canvas.create_text(width/2, lineHeight+lineHeight/2, text= 'PR Single')
averageText = canvas.create_text(width/2, 2*lineHeight+lineHeight/2, text= 'PR Average')
canvas.pack()

readThread = threading.Thread(target=dataRead.readLoop, name="readLoop", args=(canvas,nameText, singleText, averageText))
readThread.start()

root.mainloop()        