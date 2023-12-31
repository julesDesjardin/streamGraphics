import tkinter as tk
from tkinter import ttk
import json
import dataWrite, WCIFParse

def configureButton(button,camera,name,id):
    button.configure(text=name,command=lambda:dataWrite.sendData(camera,id))

def updateCubers(group,buttonsLeft,buttonsRight):
    for i in range(0,2):
        configureButton(buttonsLeft[i],0,personTest[2*(int(group)-1)+i],idTest[2*(int(group)-1)+i])
        configureButton(buttonsRight[i],1,personTest[2*(int(group)-1)+i],idTest[2*(int(group)-1)+i])


with open('./Oullins.json') as exampleJson:
    wcif = json.load(exampleJson)
competitors = WCIFParse.getCompetitors(wcif)
for personId in competitors['333-r3-g1']:
    print(wcif['persons'][personId]['name'])

root = tk.Tk()
root.title('Stream Interface')
root.geometry('500x300')

main = tk.Frame(root)
main.pack(side=tk.TOP,pady=50)

frameLeft = tk.Frame(main,highlightbackground='black',highlightthickness=2)
frameLeft.columnconfigure(0, pad=20)
frameLeft.columnconfigure(1, pad=20)
frameLeft.rowconfigure(0, pad=20)
frameLeft.rowconfigure(1, pad=20)
frameLeft.rowconfigure(2, pad=20)
frameRight = tk.Frame(main,highlightbackground='black',highlightthickness=2)
frameRight.columnconfigure(0, pad=20)
frameRight.columnconfigure(1, pad=20)
frameRight.rowconfigure(0, pad=20)
frameRight.rowconfigure(1, pad=20)
frameRight.rowconfigure(2, pad=20)
frameLeft.pack(side=tk.LEFT)
frameRight.pack(side=tk.LEFT)

ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

personTest = ['Tymon Kolasinski','Juliette Sebastien','Twan Dullemond','Sebastian Weyer']
idTest = range(0,4)

labelLeft = tk.Label(frameLeft,text='Cuber on left camera')
labelLeft.grid(column=0, row=0, columnspan=2)
labelRight = tk.Label(frameRight,text='Cuber on right camera')
labelRight.grid(column=0, row=0, columnspan=2)
buttonsLeft = []
buttonsRight = []
for i in range(0,2):
    buttonsLeft.append(tk.Button(frameLeft))
    configureButton(buttonsLeft[i],0,personTest[i],idTest[i])
    buttonsLeft[i].grid(column=i,row=1)
    buttonsRight.append(tk.Button(frameRight))
    configureButton(buttonsRight[i],1,personTest[i],idTest[i])
    buttonsRight[i].grid(column=i,row=1)

groupFrame = tk.Frame(root)
groupFrame.pack()

eventLabel = tk.Label(groupFrame,text='Event:')
eventLabel.grid(column=0,row=0,sticky=tk.E)
eventVar = tk.StringVar()
eventMenu = ttk.OptionMenu(groupFrame,eventVar,'3x3','3x3','2x2')
eventVar.set('3x3')
eventMenu.grid(column=1,row=0,sticky=tk.W)
roundLabel = tk.Label(groupFrame,text='Round:')
roundLabel.grid(column=2,row=0,sticky=tk.E)
roundVar = tk.StringVar()
roundMenu = ttk.OptionMenu(groupFrame,roundVar,'1','1','2')
roundVar.set('1')
roundMenu.grid(column=3,row=0,sticky=tk.W)
groupLabel = tk.Label(groupFrame,text='Group:')
groupLabel.grid(column=4,row=0,sticky=tk.E)
groupVar = tk.StringVar()
groupMenu = ttk.OptionMenu(groupFrame,groupVar,'1','1','2')
groupVar.set('1')
groupMenu.grid(column=5,row=0,sticky=tk.W)

groupVar.trace_add('write',lambda var,index,mode :updateCubers(groupVar.get(),buttonsLeft,buttonsRight))

root.mainloop()