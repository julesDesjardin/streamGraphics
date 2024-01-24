import tkinter as tk
from tkinter import ttk
import json
import dataWrite, WCIFParse, Settings, constants

BUTTONS_ROWS = 10
BUTTONS_COLS = 5
BUTTONS_COUNT = BUTTONS_ROWS * BUTTONS_COLS

##############################################################################
# FUNCTIONS
##############################################################################

def configureButton(button,camera,competitor,visible,row,column):
    id = competitor[0]
    seed = competitor[1]
    name = competitor[2]
    button.configure(text=f'{name}\nSeed {seed+1}',command=lambda:dataWrite.sendData(camera,id))
    if visible:
        button.grid(row=row,column=column)
    else:
        button.grid_forget()

def updateCubers(settings,event,round,group,buttonsLeft,buttonsRight):
    activities = WCIFParse.getActivities(settings.wcif)
    activityId = list(activities.keys())[list(activities.values()).index((f'{constants.EVENTS[event]}-r{round}-g{group}'))] # Get key from value in the dictionary
    competitors = WCIFParse.getCompetitors(settings.wcif,activityId,event)
    fullCompetitors = [(id, seed, settings.wcif['persons'][id]['name']) for (id, seed) in competitors]
    fullCompetitors.sort(key=lambda x:x[2])
    for i in range(0,BUTTONS_ROWS):
        for j in range(0,BUTTONS_COLS):
            index = i*BUTTONS_COLS + j
            if index < len(fullCompetitors):
                configureButton(buttonsLeft[index], 0, fullCompetitors[index], True, i + 1, j) # + 1 because row 0 is for label
                configureButton(buttonsRight[index], 1, fullCompetitors[index], True, i + 1, j)
            else:
                configureButton(buttonsLeft[index], 0, ('', 0, 0), False, i, j)
                configureButton(buttonsRight[index], 1, ('', 0, 0), False, i + 1, j)


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
frameRight = tk.Frame(main,highlightbackground='black',highlightthickness=2)
for i in range(0,BUTTONS_COLS):
    frameLeft.columnconfigure(i, pad=5)
    frameRight.columnconfigure(i, pad=5)
for i in range(0,BUTTONS_ROWS):
    frameLeft.rowconfigure(i, pad=5)
    frameRight.rowconfigure(i, pad=5)
frameLeft.pack(side=tk.LEFT)
frameRight.pack(side=tk.LEFT)

ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

personTest = ['Tymon Kolasinski','Juliette Sebastien','Twan Dullemond','Sebastian Weyer']
idTest = range(0,4)

labelLeft = tk.Label(frameLeft,text='Cuber on left camera')
labelLeft.grid(column=0, row=0, columnspan=BUTTONS_COLS)
labelRight = tk.Label(frameRight,text='Cuber on right camera')
labelRight.grid(column=0, row=0, columnspan=BUTTONS_COLS)
buttonsLeft = []
buttonsRight = []
for i in range(0,BUTTONS_COUNT):
    buttonsLeft.append(tk.Button(frameLeft,height=3,width=15,anchor=tk.W,justify=tk.LEFT))
    buttonsRight.append(tk.Button(frameRight,height=3,width=15,anchor=tk.W,justify=tk.LEFT))

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

groupVar.trace_add('write',lambda var,index,mode :updateCubers(localSettings,eventVar.get(),roundVar.get(),groupVar.get(),buttonsLeft,buttonsRight))
roundVar.trace_add('write',lambda var,index,mode :updateGroups(localSettings,eventVar.get(),roundVar.get(),groupMenu,groupVar))
eventVar.trace_add('write',lambda var,index,mode :updateRounds(localSettings,eventVar.get(),roundMenu,roundVar))

##############################################################################

root.mainloop()