import tkinter as tk
from tkinter import ttk
import json
import dataWrite, WCIFParse, InterfaceSettings, constants

BUTTONS_ROWS = 10
BUTTONS_COLS = 5
BUTTONS_COUNT = BUTTONS_ROWS * BUTTONS_COLS

##############################################################################
# FUNCTIONS
##############################################################################

def configureButton(button,event,round,camera,competitor,visible,row,column,bg,fg):
    if int(round) > 1:
        previousRound = int(round) - 1
    else:
        previousRound = None
    id = competitor[0]
    seed = competitor[1]
    name = competitor[2]
    previousRank = WCIFParse.getRoundRank(localSettings.wcif,id,event,round)
    extraButtonText = f'Seed {seed}'
    if previousRank is not None:
        extraButtonText = extraButtonText + f', Placed {previousRank}'
    cardData = localSettings.cardText
    cardData = cardData.replace('%name',f"{name}")
    prSingleInt = WCIFParse.getPb(localSettings.wcif,id,event,'single')
    prAverageInt = WCIFParse.getPb(localSettings.wcif,id,event,'average')
    cardData = cardData.replace('%prSingle',dataWrite.resultToString(prSingleInt))
    cardData = cardData.replace('%prAverage',dataWrite.resultToString(prAverageInt))
    cardData = cardData.replace('%nrSingle',f"{WCIFParse.getRanking(localSettings.wcif,id,event,'single','national')}")
    cardData = cardData.replace('%nrAverage',f"{WCIFParse.getRanking(localSettings.wcif,id,event,'average','national')}")
    cardData = cardData.replace('%crSingle',f"{WCIFParse.getRanking(localSettings.wcif,id,event,'single','continental')}")
    cardData = cardData.replace('%crAverage',f"{WCIFParse.getRanking(localSettings.wcif,id,event,'average','continental')}")
    cardData = cardData.replace('%wrSingle',f"{WCIFParse.getRanking(localSettings.wcif,id,event,'single','world')}")
    cardData = cardData.replace('%wrAverage',f"{WCIFParse.getRanking(localSettings.wcif,id,event,'average','world')}")
    cardData = cardData.replace('%seed',f"{seed}")
    cardData = cardData.replace('%previousRank',f"{previousRank}")
    cardData = cardData.replace('%previousSingle',dataWrite.resultToString(WCIFParse.getRoundResult(localSettings.wcif,id,event,round,'single')))
    cardData = cardData.replace('%previousAverage',dataWrite.resultToString(WCIFParse.getRoundResult(localSettings.wcif,id,event,round,'average')))
    button.configure(text=f'{name}\n{extraButtonText}',command=lambda:dataWrite.sendCardData(localSettings.bot,camera,cardData),bg=bg,fg=fg)
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
        competitors = WCIFParse.getCompetitors(settings.wcif,activityId,event)
        fullCompetitors = [(id, seed, settings.wcif['persons'][id]['name']) for (id, seed) in competitors]
        fullCompetitors.sort(key=lambda x:x[2])
        for i in range(0,BUTTONS_ROWS):
            for j in range(0,BUTTONS_COLS):
                buttonIndex = i*BUTTONS_COLS + j
                while index < len(fullCompetitors) and fullCompetitors[index][1] > settings.maxSeed: # Search next competitor within max seed
                    index = index + 1
                if index < len(fullCompetitors):
                    configureButton(buttonsLeft[buttonIndex], event, round, 0, fullCompetitors[index], True, i + 1, j, bg, fg) # + 1 because row 0 is for label
                    configureButton(buttonsRight[buttonIndex], event, round, 1, fullCompetitors[index], True, i + 1, j, bg, fg)
                    index = index + 1
                else:
                    configureButton(buttonsLeft[buttonIndex], event, round, 0, (0, 0, ''), False, i, j, bg, fg)
                    configureButton(buttonsRight[buttonIndex], event, round, 1, (0, 0, ''), False, i + 1, j, bg, fg)

def OKButtonCommand(updateTimeTower,settings,buttonsLeft,buttonsRight):
    if updateTimeTower:
        event = settings.stages[0].eventVar.get()
        round = settings.stages[0].roundVar.get()
        dataWrite.sendTimeTowerEvent(settings.bot,constants.EVENTS[event],round)
    updateCubers(settings,buttonsLeft,buttonsRight)

##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Interface')

##############################################################################
# SETTINGS
##############################################################################

localSettings = InterfaceSettings.InterfaceSettings(root)
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
TimeTowerVariable = tk.IntVar()
TimeTowerCheckbox = tk.Checkbutton(OKFrame, text="Update TimeTower", variable=TimeTowerVariable)
TimeTowerCheckbox.pack()
OKButton = tk.Button(OKFrame, text="OK", command=lambda:OKButtonCommand(TimeTowerVariable.get(),localSettings,buttonsLeft,buttonsRight))
OKButton.pack()

##############################################################################

root.mainloop()