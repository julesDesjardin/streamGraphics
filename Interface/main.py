import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import json
import dataWrite
import WCIFParse
import InterfaceSettings
import constants
import PresentationInterface

BUTTONS_ROWS = 4
BUTTONS_COLS = 7
BUTTONS_COUNT = BUTTONS_ROWS * BUTTONS_COLS
CAMERAS_ROWS = 2
CAMERAS_COLS = 2
CAMERAS_COUNT = CAMERAS_ROWS * CAMERAS_COLS

##############################################################################
# FUNCTIONS
##############################################################################


def buttonCommand(camera, buttonIndex, bot, cardData, competitorId):
    for index in range(len(buttons[camera])):
        if index == buttonIndex:
            buttons[camera][index].configure(relief=tk.SUNKEN)
        else:
            buttons[camera][index].configure(relief=tk.RAISED)
    dataWrite.sendCardData(bot, camera, cardData)
    if timeTowerVariables[camera].get() == 1:
        dataWrite.sendTimeTowerExpand(bot, WCIFParse.getRegistrantId(localSettings.wcif, activeCubers[camera]), 0)
        dataWrite.sendTimeTowerExpand(bot, WCIFParse.getRegistrantId(localSettings.wcif, competitorId), 1)
    activeCubers[camera] = competitorId


def configureButton(camera, buttonIndex, event, round, competitor, visible, row, column, bg, fg):
    if not visible:
        buttons[camera][buttonIndex].grid_forget()
    else:
        if int(round) > 1:
            previousRound = int(round) - 1
        else:
            previousRound = None
        id = competitor[0]
        seed = competitor[1]
        name = competitor[2]
        previousRank = WCIFParse.getRoundRank(localSettings.wcif, id, event, previousRound)
        extraButtonText = f'Seed {seed}'
        if previousRank is not None:
            extraButtonText = extraButtonText + f', Placed {previousRank}'
        cardData = WCIFParse.getCountry(localSettings.wcif, id) + ' ' + localSettings.cardText
        cardData = cardData.replace('%name', f"{name}")
        prSingleInt = WCIFParse.getPb(localSettings.wcif, id, event, 'single')
        prAverageInt = WCIFParse.getPb(localSettings.wcif, id, event, 'average')
        cardData = cardData.replace('%prSingle', dataWrite.resultToString(prSingleInt))
        cardData = cardData.replace('%prAverage', dataWrite.resultToString(prAverageInt))
        cardData = cardData.replace('%nrSingle', f"{WCIFParse.getRanking(localSettings.wcif,id,event,'single','national')}")
        cardData = cardData.replace('%nrAverage', f"{WCIFParse.getRanking(localSettings.wcif,id,event,'average','national')}")
        cardData = cardData.replace('%crSingle', f"{WCIFParse.getRanking(localSettings.wcif,id,event,'single','continental')}")
        cardData = cardData.replace('%crAverage', f"{WCIFParse.getRanking(localSettings.wcif,id,event,'average','continental')}")
        cardData = cardData.replace('%wrSingle', f"{WCIFParse.getRanking(localSettings.wcif,id,event,'single','world')}")
        cardData = cardData.replace('%wrAverage', f"{WCIFParse.getRanking(localSettings.wcif,id,event,'average','world')}")
        cardData = cardData.replace('%seed', f"{seed}")
        cardData = cardData.replace('%previousRank', f"{previousRank}")
        cardData = cardData.replace('%previousSingle', dataWrite.resultToString(
            WCIFParse.getRoundResult(localSettings.wcif, id, event, round, 'single')))
        cardData = cardData.replace('%previousAverage', dataWrite.resultToString(
            WCIFParse.getRoundResult(localSettings.wcif, id, event, round, 'average')))
        buttons[camera][buttonIndex].configure(text=f'{name}\n{extraButtonText}', command=lambda: buttonCommand(
            camera, buttonIndex, localSettings.bot, cardData, id), bg=bg, fg=fg)
        buttons[camera][buttonIndex].grid(row=row, column=column)


def updateCubers(settings, buttons):
    index = 0
    fullCompetitors = []
    bg = []
    fg = []
    events = []
    rounds = []
    for stage in settings.stages:
        if stage.stageEnabled:
            activities = WCIFParse.getActivities(settings.wcif, stage.venue, stage.room)
            event = stage.eventVar.get()
            round = stage.roundVar.get()
            group = stage.groupVar.get()
            if group != '0':
                activityId = WCIFParse.getActivityId(settings.wcif, stage.venue, stage.room, event, round, group)
                competitors = WCIFParse.getCompetitors(settings.wcif, activityId, event)
                newCompetitors = [(id, seed, WCIFParse.getCompetitorName(settings.wcif, id)) for (id, seed) in competitors]
                newCompetitors.sort(key=lambda x: x[2])
                for competitor in newCompetitors:
                    if competitor[1] <= settings.maxSeed:
                        fullCompetitors.append(competitor)
                        bg.append(stage.backgroundColor)
                        fg.append(stage.textColor)
                        events.append(event)
                        rounds.append(round)

    # If too many competitors : keep top X only
    sortedCompetitors = sorted(fullCompetitors, key=lambda x: x[1])
    if len(sortedCompetitors) > BUTTONS_COUNT:
        for competitor in sortedCompetitors[BUTTONS_COUNT:]:
            indexCompetitor = fullCompetitors.index(competitor)
            del fullCompetitors[indexCompetitor]
            del bg[indexCompetitor]
            del fg[indexCompetitor]
            del events[indexCompetitor]
            del rounds[indexCompetitor]

    for i in range(0, BUTTONS_ROWS):
        for j in range(0, BUTTONS_COLS):
            buttonIndex = i * BUTTONS_COLS + j
            if index < len(fullCompetitors):
                for camera in range(0, CAMERAS_COUNT):
                    configureButton(camera, buttonIndex, events[index], rounds[index], fullCompetitors[index], True,
                                    i + 2, j, bg[index], fg[index])  # + 2 because row 0 is for label and row 1 is for clean
                index = index + 1
            else:
                for camera in range(0, CAMERAS_COUNT):
                    configureButton(camera, buttonIndex, '', '', (0, 0, ''), False, i + 2, j, '#000000', '#000000')


def getStageInfo(settings):
    for stage in settings.stages:
        if stage.stageEnabled:
            return (stage.venue, stage.room, stage.eventVar.get(), stage.roundVar.get(), stage.groupVar.get())
    tkinter.messagebox.showerror(
        title='Stages error !', message='All stages are disabled (or no stages exist), please enable a stage')
    return (None, None, None, None, None)


def OKButtonCommand(updateTimeTower, settings, buttons):
    if updateTimeTower:
        (_, _, event, round, _) = getStageInfo(settings)
        if event is not None:
            dataWrite.sendTimeTowerEvent(settings.bot, constants.EVENTS[event], round)
    updateCubers(settings, buttons)
    for camera in range(0, CAMERAS_COUNT):
        buttonCommand(camera, -1, localSettings.bot, '', -1)


def timeTowerCommand(bot, camera):
    dataWrite.sendTimeTowerExpand(bot, WCIFParse.getRegistrantId(localSettings.wcif, activeCubers[camera]), timeTowerVariables[camera].get())


def presentationButtonCommand(settings):
    (venue, room, event, round, group) = getStageInfo(settings)
    if event is not None:
        presentation = PresentationInterface.PresentationInterface(settings.root, settings.wcif, venue, room, event, int(round), group, settings.bot)


##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Interface')
root.state('zoomed')

##############################################################################
# SETTINGS
##############################################################################

localSettings = InterfaceSettings.InterfaceSettings(root)
localSettings.showFrame()

##############################################################################
# MAIN
##############################################################################

main = tk.Frame(root)
main.pack(side=tk.TOP, padx=10)

main.grid_columnconfigure(0, minsize=800)
main.grid_columnconfigure(1, minsize=800)
main.grid_rowconfigure(0, minsize=270)
main.grid_rowconfigure(1, minsize=270)

framesButtons = []
labelsButtons = []
buttons = []
activeCubers = []
timeTowerVariables = []
timeTowerButtons = []
cleanButtons = []
for camera in range(0, CAMERAS_COUNT):
    activeCubers.append(-1)
    framesButtons.append(tk.Frame(main, highlightbackground='black', highlightthickness=2))
    labelsButtons.append(tk.Label(framesButtons[camera], text=f'Cuber on camera {camera+1}'))
    labelsButtons[camera].grid(column=0, row=0, columnspan=BUTTONS_COLS)
    timeTowerVariables.append(tk.IntVar())
    timeTowerButtons.append(tk.Checkbutton(framesButtons[camera], text='Expand TimeTower line', variable=timeTowerVariables[camera],
                            command=lambda localCamera=camera: timeTowerCommand(localSettings.bot, localCamera)))
    timeTowerButtons[camera].grid(column=0, row=1, columnspan=3, sticky='e')
    cleanButtons.append(tk.Button(framesButtons[camera]))
    # localCamera is a trick for the lambda function, since "camera" is a global variable it wouldn't get the value from the loop
    cleanButtons[camera].configure(text=f'Clean', command=lambda localCamera=camera: buttonCommand(localCamera, -1, localSettings.bot, '', -1))
    cleanButtons[camera].grid(column=3, row=1)
    buttons.append([])
    for button in range(0, BUTTONS_COLS + 2):
        framesButtons[camera].columnconfigure(button, pad=5)
    for button in range(0, BUTTONS_ROWS):
        framesButtons[camera].rowconfigure(button, pad=5)

    for button in range(0, BUTTONS_COUNT):
        buttons[camera].append(tk.Button(framesButtons[camera], height=2, width=15, anchor=tk.W, justify=tk.LEFT))

for cameraRow in range(0, CAMERAS_ROWS):
    for cameraCol in range(0, CAMERAS_COLS):
        framesButtons[cameraRow * CAMERAS_COLS + cameraCol].grid(column=cameraCol, row=cameraRow, sticky='nsew')

ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

##############################################################################
# CHOOSE GROUP
##############################################################################

OKFrame = tk.Frame(root)
OKFrame.pack(side=tk.BOTTOM, pady=20)
TimeTowerVariable = tk.IntVar()
TimeTowerCheckbox = tk.Checkbutton(OKFrame, text="Update TimeTower", variable=TimeTowerVariable)
TimeTowerCheckbox.pack()
OKButton = tk.Button(OKFrame, text="OK", command=lambda: OKButtonCommand(TimeTowerVariable.get(), localSettings, buttons))
OKButton.pack()
presentationButton = tk.Button(OKFrame, text='Start presentation', command=lambda: presentationButtonCommand(localSettings))
presentationButton.pack(pady=30)

##############################################################################

root.mainloop()
