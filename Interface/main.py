import tkinter as tk
from tkinter import ttk
import json
import dataWrite, WCIFParse, Settings, constants

##############################################################################
# FUNCTIONS
##############################################################################

def configureButton(button,camera,name,id):
    button.configure(text=name,command=lambda:dataWrite.sendData(camera,id))

def updateCubers(group,buttonsLeft,buttonsRight):
    for i in range(0,2):
        configureButton(buttonsLeft[i],0,personTest[2*(int(group)-1)+i],idTest[2*(int(group)-1)+i])
        configureButton(buttonsRight[i],1,personTest[2*(int(group)-1)+i],idTest[2*(int(group)-1)+i])

def updateGroups(settings,event,round,groupMenu,groupVar):
    activities = WCIFParse.getActivities(settings.wcif)
    maxGroup = 0
    for activity in activities:
        activitySplit = activities[activity].split('-')
        if activitySplit[0] == constants.EVENTS[event] and activitySplit[1] == f'r{round}':
            maxGroup = max(maxGroup,int(activitySplit[2][1:]))
    menu = groupMenu["menu"]
    menu.delete(0, "end")
    if maxGroup > 0:
        for i in range(1,maxGroup+1):
            menu.add_command(label=f'{i}',command=lambda value=f'{i}': groupVar.set(value))
        groupVar.set(1)

def updateRounds(settings,event,roundMenu,roundVar):
    activities = WCIFParse.getActivities(settings.wcif)
    maxRound = 0
    for activity in activities:
        activitySplit = activities[activity].split('-')
        if activitySplit[0] == constants.EVENTS[event]:
            maxRound = max(maxRound,int(activitySplit[1][1:]))
    menu = roundMenu["menu"]
    menu.delete(0, "end")
    if maxRound > 0:
        for i in range(1,maxRound+1):
            menu.add_command(label=f'{i}',command=lambda value=f'{i}': roundVar.set(value))
        roundVar.set(1)


##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Interface')

##############################################################################
# SETTINGS
##############################################################################

localSettings = Settings.Settings(root)
localSettings.showFrame()

##############################################################################
# MAIN
##############################################################################

main = tk.Frame(root)
main.pack(side=tk.TOP,padx=50,pady=50)

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

##############################################################################
# CHOOSE GROUP
##############################################################################

groupFrame = tk.Frame(root,padx=50,pady=20)
groupFrame.pack()

eventLabel = tk.Label(groupFrame,text='Event:')
eventLabel.grid(column=0,row=0,sticky=tk.E)
eventVar = tk.StringVar()
eventMenu = ttk.OptionMenu(groupFrame,eventVar,list(constants.EVENTS.keys())[0],*list(constants.EVENTS.keys()))
eventMenu.grid(column=1,row=0,sticky=tk.W)
roundLabel = tk.Label(groupFrame,text='Round:')
roundLabel.grid(column=2,row=0,sticky=tk.E)
roundVar = tk.StringVar()
roundMenu = ttk.OptionMenu(groupFrame,roundVar)
roundMenu.grid(column=3,row=0,sticky=tk.W)
groupLabel = tk.Label(groupFrame,text='Group:')
groupLabel.grid(column=4,row=0,sticky=tk.E)
groupVar = tk.StringVar()
groupMenu = ttk.OptionMenu(groupFrame,groupVar)
groupMenu.grid(column=5,row=0,sticky=tk.W)

groupVar.trace_add('write',lambda var,index,mode :updateCubers(groupVar.get(),buttonsLeft,buttonsRight))
roundVar.trace_add('write',lambda var,index,mode :updateGroups(localSettings,eventVar.get(),roundVar.get(),groupMenu,groupVar))
eventVar.trace_add('write',lambda var,index,mode :updateRounds(localSettings,eventVar.get(),roundMenu,roundVar))

##############################################################################

root.mainloop()