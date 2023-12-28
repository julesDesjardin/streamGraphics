import tkinter as tk
from tkinter import ttk
import dataWrite

def configureButton(button,name,id):
    button.configure(text=name,command=lambda:dataWrite.sendData(id))

def updateCubers(group,buttons):
    for i in range(0,2):
        configureButton(buttons[i],personTest[2*(int(group)-1)+i],idTest[2*(int(group)-1)+i])
    
root = tk.Tk()
root.title('Stream Interface')
root.geometry('500x400')

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
buttons = []
for i in range(0,2):
    buttons.append(tk.Button(main))
    configureButton(buttons[i],personTest[i],idTest[i])
    buttons[i].grid(column=i,row=1)

groupFrame = tk.Frame(root)
groupFrame.pack(pady=100)

eventLabel = tk.Label(groupFrame,text='Event:')
eventLabel.grid(column=0,row=0,sticky=tk.E)
eventVar = tk.StringVar()
eventMenu = tk.OptionMenu(groupFrame,eventVar,'3x3','2x2')
eventVar.set('3x3')
eventMenu.grid(column=1,row=0,sticky=tk.W)
roundLabel = tk.Label(groupFrame,text='Round:')
roundLabel.grid(column=2,row=0,sticky=tk.E)
roundVar = tk.StringVar()
roundMenu = tk.OptionMenu(groupFrame,roundVar, '1','2')
roundVar.set('1')
roundMenu.grid(column=3,row=0,sticky=tk.W)
groupLabel = tk.Label(groupFrame,text='Round:')
groupLabel.grid(column=4,row=0,sticky=tk.E)
groupVar = tk.StringVar()
groupMenu = tk.OptionMenu(groupFrame,groupVar, '1','2')
groupVar.set('1')
groupMenu.grid(column=5,row=0,sticky=tk.W)

groupVar.trace_add('write',lambda var,index,mode :updateCubers(groupVar.get(),buttons))

root.mainloop()