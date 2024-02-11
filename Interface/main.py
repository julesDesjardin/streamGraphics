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

def configureButton(button,camera,competitor,visible,row,column,bg,fg):
    id = competitor[0]
    seed = competitor[1]
    name = competitor[2]
    rank = competitor[3]
    extraText = f'Seed {seed}'
    if rank is not None:
        extraText = extraText + f', Placed {rank}'
    button.configure(text=f'{name}\n{extraText}',command=lambda:dataWrite.sendData(camera,id),bg=bg,fg=fg)
    if visible:
        button.grid(row=row,column=column)
    else:
        button.grid_forget()

def updateCubers(settings,buttonsLeft,buttonsRight):
    activities = WCIFParse.getActivities(settings.wcif)
    index = 0
    for stage in settings.stages:
        event = stage.eventVar.get()
        round = stage.roundVar.get()
        group = stage.groupVar.get()
        bg = stage.backgroundColor
        fg = stage.textColor
        activityId = list(activities.keys())[list(activities.values()).index((f'{constants.EVENTS[event]}-r{round}-g{group}'))] # Get key from value in the dictionary
        if int(round) > 1:
            previousRound = int(round) - 1
        else:
            previousRound = None
        competitors = WCIFParse.getCompetitors(settings.wcif,activityId,event)
        fullCompetitors = [(id, seed, settings.wcif['persons'][id]['name'], WCIFParse.getRoundRank(settings.wcif, id, event, previousRound)) for (id, seed) in competitors]
        fullCompetitors.sort(key=lambda x:x[2])
        for i in range(0,BUTTONS_ROWS):
            for j in range(0,BUTTONS_COLS):
                buttonIndex = i*BUTTONS_COLS + j
                while index < len(fullCompetitors) and fullCompetitors[index][1] > settings.maxSeed: # Search next competitor within max seed
                    index = index + 1
                if index < len(fullCompetitors):
                    configureButton(buttonsLeft[buttonIndex], 0, fullCompetitors[index], True, i + 1, j, bg, fg) # + 1 because row 0 is for label
                    configureButton(buttonsRight[buttonIndex], 1, fullCompetitors[index], True, i + 1, j, bg, fg)
                    index = index + 1
                else:
                    configureButton(buttonsLeft[buttonIndex], 0, ('', 0, 0, 0), False, i, j, bg, fg)
                    configureButton(buttonsRight[buttonIndex], 1, ('', 0, 0, 0), False, i + 1, j, bg, fg)

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

OKFrame = tk.Frame(root)
OKFrame.pack(side=tk.BOTTOM,pady=20)
OKButton = tk.Button(OKFrame, text="OK", command=lambda:updateCubers(localSettings,buttonsLeft,buttonsRight))
OKButton.pack()

##############################################################################

root.mainloop()