import tkinter as tk
import tkinter.messagebox
import json
import dataWrite
import WCIFParse
import InterfaceSettings
import utils
import PresentationInterface


##############################################################################
# FUNCTIONS
##############################################################################

def configureButton(frame, buttonIndex, event, round, competitor, visible, row, column, bg, fg):
    if not visible:
        frame.buttonFrames[buttonIndex].grid_forget()
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
        cardText = utils.replaceText(localSettings.cardText, localSettings.wcif, id, seed, event, round)
        frame.buttons[buttonIndex].configure(text=f'{name}\n{extraButtonText}', bg=bg, fg=fg, command=lambda: frame.buttonCommand(
            buttonIndex, WCIFParse.getCountry(localSettings.wcif, id), name, WCIFParse.getAvatar(localSettings.wcif, id), cardText, id))
        frame.buttonFrames[buttonIndex].grid(row=row, column=column)


def updateCubers(settings):
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
    if len(sortedCompetitors) > settings.buttonCount:
        for competitor in sortedCompetitors[settings.buttonCount:]:
            indexCompetitor = fullCompetitors.index(competitor)
            del fullCompetitors[indexCompetitor]
            del bg[indexCompetitor]
            del fg[indexCompetitor]
            del events[indexCompetitor]
            del rounds[indexCompetitor]

    for i in range(0, settings.buttonRows):
        for j in range(0, settings.buttonCols):
            buttonIndex = i * settings.buttonCols + j
            if index < len(fullCompetitors):
                for frame in settings.interfaceFrames:
                    configureButton(frame, buttonIndex, events[index], rounds[index], fullCompetitors[index], True,
                                    i + 3, j, bg[index], fg[index])
                index = index + 1
            else:
                for frame in settings.interfaceFrames:
                    configureButton(frame, buttonIndex, '', '', (0, 0, ''), False, i + 3, j, '#000000', '#000000')


def getStageInfo(settings):
    for stage in settings.stages:
        if stage.stageEnabled:
            return (stage.venue, stage.room, stage.eventVar.get(), stage.roundVar.get(), stage.groupVar.get())
    tkinter.messagebox.showerror(
        title='Stages error !', message='All stages are disabled (or no stages exist), please enable a stage')
    return (None, None, None, None, None)


def OKButtonCommand(updateTimeTower, settings):
    if updateTimeTower:
        (_, _, event, round, _) = getStageInfo(settings)
        if event is not None:
            dataWrite.sendTimeTowerEvent(settings.bot, utils.EVENTS[event], round)
    updateCubers(settings)
    for frame in settings.interfaceFrames:
        frame.buttonCommand(-1, '', '', '', '', -1)


def presentationButtonCommand(settings):
    (venue, room, event, round, group) = getStageInfo(settings)
    if event is not None:
        presentation = PresentationInterface.PresentationInterface(
            settings.root, settings.wcif, settings.presentationText, venue, room, event, int(round), group, settings.bot)


##############################################################################
# ROOT
##############################################################################

root = tk.Tk()
root.title('Stream Interface')

##############################################################################
# MAIN
##############################################################################

main = tk.Frame(root)

##############################################################################
# SETTINGS
##############################################################################

localSettings = InterfaceSettings.InterfaceSettings(root, main)
localSettings.showFrame()

##############################################################################
# CHOOSE GROUP
##############################################################################

OKFrame = tk.Frame(root)
OKFrame.pack(side=tk.BOTTOM, pady=20)
TimeTowerVariable = tk.IntVar()
TimeTowerCheckbox = tk.Checkbutton(OKFrame, text="Update TimeTower", variable=TimeTowerVariable)
TimeTowerCheckbox.pack()
OKButton = tk.Button(OKFrame, text="OK", command=lambda: OKButtonCommand(TimeTowerVariable.get(), localSettings))
OKButton.pack()
presentationButton = tk.Button(OKFrame, text='Start presentation', command=lambda: presentationButtonCommand(localSettings))
presentationButton.pack(pady=30)

##############################################################################

main.pack(side=tk.TOP, padx=10)
root.mainloop()
