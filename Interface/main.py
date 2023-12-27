import tkinter as tk
from tkinter import ttk
import dataWrite

def createButton(frame,name,id):
    return ttk.Button(frame,text=name,command=lambda:dataWrite.sendData(id))

root = tk.Tk()
root.title('Stream Interface')

main = tk.Frame(root)
main.pack()
main.columnconfigure(0, pad=20)
main.columnconfigure(1, pad=20)
main.rowconfigure(0, pad=20)
main.rowconfigure(1, pad=20)
main.rowconfigure(2, pad=20)

ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

personTest = ['Tymon Kolasinski','Juliette Sebastien','Twan Dullemond','Sebastian Weyer']
idTest = range(0,4)

title = ttk.Label(main,text='Choose a cuber')
title.grid(column=0, row=0, columnspan=2)
for i in range(0,4):
    button = createButton(main,personTest[i],idTest[i])
    button.grid(column=i % 2,row=1+int(i/2))
    
root.mainloop()