import tkinter as tk
from tkinter import ttk
import json
import dataWrite, WCIFParse, InterfaceSettings, constants

BUTTONS_ROWS = 10
BUTTONS_COLS = 5
BUTTONS_COUNT = BUTTONS_ROWS * BUTTONS_COLS
CAMERAS_ROWS = 2
CAMERAS_COLS = 2
CAMERAS_COUNT = CAMERAS_ROWS * CAMERAS_COLS

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

def updateCubers(settings,buttons):
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
                    for camera in range(0,CAMERAS_COUNT):
                        configureButton(buttons[camera][buttonIndex], event, round, camera, fullCompetitors[index], True, i + 1, j, bg, fg) # + 1 because row 0 is for label
                    index = index + 1
                else:
                    for camera in range(0,CAMERAS_COUNT):
                        configureButton(buttons[camera][buttonIndex], event, round, camera, (0, 0, ''), False, i, j, bg, fg)

def OKButtonCommand(updateTimeTower,settings,buttons):
    if updateTimeTower:
        event = settings.stages[0].eventVar.get()
        round = settings.stages[0].roundVar.get()
        dataWrite.sendTimeTowerEvent(settings.bot,constants.EVENTS[event],round)
    updateCubers(settings,buttons)

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

framesButtons = []
labelsButtons = []
buttons = []
for camera in range(0, CAMERAS_COUNT):
    framesButtons.append(tk.Frame(main,highlightbackground='black',highlightthickness=2))
    labelsButtons.append(tk.Label(framesButtons[camera], text=f'Cuber on camera {camera+1}'))
    labelsButtons[camera].grid(column=0, row=0, columnspan=BUTTONS_COLS)
    buttons.append([])
    for button in range(0,BUTTONS_COLS):
        framesButtons[camera].columnconfigure(button, pad=5)
    for button in range(0,BUTTONS_ROWS):
        framesButtons[camera].rowconfigure(button, pad=5)

    for button in range(0,BUTTONS_COUNT):
        buttons[camera].append(tk.Button(framesButtons[camera],height=3,width=15,anchor=tk.W,justify=tk.LEFT))

for cameraRow in range(0,CAMERAS_ROWS):
    for cameraCol in range(0,CAMERAS_COLS):
        framesButtons[cameraRow*CAMERAS_COLS + cameraCol].grid(column=cameraCol, row=cameraRow)

ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

##############################################################################
# CHOOSE GROUP
##############################################################################

OKFrame = tk.Frame(root)
OKFrame.pack(side=tk.BOTTOM,pady=20)
TimeTowerVariable = tk.IntVar()
TimeTowerCheckbox = tk.Checkbutton(OKFrame, text="Update TimeTower", variable=TimeTowerVariable)
TimeTowerCheckbox.pack()
OKButton = tk.Button(OKFrame, text="OK", command=lambda:OKButtonCommand(TimeTowerVariable.get(),localSettings,buttons))
OKButton.pack()

##############################################################################

root.mainloop()