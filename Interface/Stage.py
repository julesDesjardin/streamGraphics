import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import WCIFParse
import interfaceUtils

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common.commonUtils import colorButtonCommand, getTextColorFromBackground


class Stage:

    def __init__(self, root, wcif, backgroundColor, textColor, venue, room):
        self.root = root
        self.wcif = wcif
        self.backgroundColor = backgroundColor
        self.textColor = textColor
        self.venue = venue
        self.room = room
        self.frame = tk.Frame(self.root, bg=self.backgroundColor, highlightbackground='black', highlightthickness=1, padx=50, pady=5)
        self.disableButton = tk.Button(self.frame, text='Disable stage', command=self.disableStageToggle)
        self.disableButton.grid(column=0, row=0)
        self.eventLabel = tk.Label(self.frame, text='Event:', bg=self.backgroundColor, fg=self.textColor,
                                   activebackground=self.backgroundColor, activeforeground=self.textColor)
        self.eventLabel.grid(column=1, row=0, sticky=tk.E)
        self.eventVar = tk.StringVar()
        self.eventMenu = ttk.OptionMenu(self.frame, self.eventVar, list(interfaceUtils.EVENTS.keys())[0], *list(interfaceUtils.EVENTS.keys()))
        self.eventMenu.grid(column=2, row=0, sticky=tk.W)
        self.roundLabel = tk.Label(self.frame, text='Round:', bg=self.backgroundColor, fg=self.textColor,
                                   activebackground=self.backgroundColor, activeforeground=self.textColor)
        self.roundLabel.grid(column=3, row=0, sticky=tk.E)
        self.roundVar = tk.StringVar()
        self.roundMenu = ttk.OptionMenu(self.frame, self.roundVar)
        self.roundMenu.grid(column=4, row=0, sticky=tk.W)
        self.groupLabel = tk.Label(self.frame, text='Group:', bg=self.backgroundColor, fg=self.textColor,
                                   activebackground=self.backgroundColor, activeforeground=self.textColor)
        self.groupLabel.grid(column=5, row=0, sticky=tk.E)
        self.groupVar = tk.StringVar()
        self.groupMenu = ttk.OptionMenu(self.frame, self.groupVar)
        self.groupMenu.grid(column=6, row=0, sticky=tk.W)
        self.stageEnabled = True

        self.roundVar.trace_add('write', lambda var, index, mode: self.updateGroups())
        self.eventVar.trace_add('write', lambda var, index, mode: self.updateRounds())
        self.eventVar.set('3x3x3')

    def disableStageToggle(self):
        if self.stageEnabled:
            self.stageEnabled = False
            self.disableButton.configure(relief=tk.SUNKEN)
            self.eventLabel.configure(state='disabled')
            self.eventMenu.configure(state='disabled')
            self.roundLabel.configure(state='disabled')
            self.roundMenu.configure(state='disabled')
            self.groupLabel.configure(state='disabled')
            self.groupMenu.configure(state='disabled')
        else:
            self.stageEnabled = True
            self.disableButton.configure(relief=tk.RAISED)
            self.eventLabel.configure(state='active')
            self.eventMenu.configure(state='active')
            self.roundLabel.configure(state='active')
            self.roundMenu.configure(state='active')
            self.groupLabel.configure(state='active')
            self.groupMenu.configure(state='active')

    def updateGroups(self):
        activities = WCIFParse.getActivities(self.wcif, self.venue, self.room)
        groups = []
        for activity in activities:
            activitySplit = activities[activity].split('-')
            if activitySplit[0] == interfaceUtils.EVENTS[self.eventVar.get()] and activitySplit[1] == f'r{self.roundVar.get()}':
                groups.append(int(activitySplit[2][1:]))
        menu = self.groupMenu["menu"]
        menu.delete(0, "end")
        if len(groups) > 0:
            for group in sorted(groups):
                menu.add_command(label=f'{group}', command=lambda value=f'{group}': self.groupVar.set(value))
            self.groupVar.set(sorted(groups)[0])
        else:
            menu.add_command(label='No group', command=lambda value=0: self.roundVar.set(value))
            self.groupVar.set(0)

    def updateRounds(self):
        activities = WCIFParse.getActivities(self.wcif, self.venue, self.room)
        rounds = []
        for activity in activities:
            activitySplit = activities[activity].split('-')
            if activitySplit[0] == interfaceUtils.EVENTS[self.eventVar.get()]:
                newRound = int(activitySplit[1][1:])
                if newRound not in rounds:
                    rounds.append(newRound)
        menu = self.roundMenu["menu"]
        menu.delete(0, "end")
        if len(rounds) > 0:
            for round in sorted(rounds):
                menu.add_command(label=f'{round}', command=lambda value=f'{round}': self.roundVar.set(value))
            self.roundVar.set(sorted(rounds)[0])
        else:
            menu.add_command(label='No round', command=lambda value=0: self.roundVar.set(value))
            self.roundVar.set(0)

    def hideStage(self):
        self.frame.pack_forget()

    def showStage(self):
        self.frame.pack(side=tk.BOTTOM)

    def setEvent(self, event):
        self.eventVar.set(event)

    def setRound(self, round):
        self.roundVar.set(round)

    def updateRoomMenu(self, venueVar, roomMenu, roomVar):
        menu = roomMenu['menu']
        menu.delete(0, 'end')
        rooms = WCIFParse.getRooms(self.wcif, WCIFParse.getVenueId(self.wcif, venueVar.get()))
        for room in rooms:
            menu.add_command(label=room, command=lambda value=room: roomVar.set(value))
        roomVar.set(rooms[0])

    def updateWindowCloseButton(self, venue, room, color, window):
        self.venue = WCIFParse.getVenueId(self.wcif, venue)
        self.room = WCIFParse.getRoomId(self.wcif, self.venue, room)
        self.backgroundColor = color
        self.textColor = getTextColorFromBackground(self.backgroundColor)
        self.frame.configure(bg=self.backgroundColor)
        self.eventLabel.configure(bg=self.backgroundColor, fg=self.textColor)
        self.roundLabel.configure(bg=self.backgroundColor, fg=self.textColor)
        self.groupLabel.configure(bg=self.backgroundColor, fg=self.textColor)
        self.eventVar.set('3x3x3')  # Will reload rounds and groups in the display
        window.destroy()

    def updateWindow(self, root, addNewStage):
        window = tk.Toplevel(root)
        window.grab_set()
        if addNewStage:
            titleLabel = tk.Label(window, text='Configure new stage')
        else:
            titleLabel = tk.Label(window, text='Edit stage')
        titleLabel.grid(row=0, column=0, columnspan=2)
        venueLabel = tk.Label(window, text='Venue')
        venueLabel.grid(sticky='E', row=1, column=0)
        venueVar = tk.StringVar()
        venueMenu = ttk.OptionMenu(window, venueVar, WCIFParse.getVenueName(self.wcif, self.venue), *WCIFParse.getVenues(self.wcif))
        venueMenu.grid(sticky='W', row=1, column=1)
        roomLabel = tk.Label(window, text='Room')
        roomLabel.grid(sticky='E', row=2, column=0)
        roomVar = tk.StringVar()
        roomMenu = ttk.OptionMenu(window, roomVar, WCIFParse.getRoomName(
            self.wcif, self.venue, self.room), *WCIFParse.getRooms(self.wcif, self.venue))
        roomMenu.grid(sticky='W', row=2, column=1)
        venueVar.trace_add('write', lambda var, index, mode: self.updateRoomMenu(venueVar, roomMenu, roomVar))

        getColorScheduleButton = tk.Button(window, text='Get color from schedule',
                                           command=lambda: bgColorVariable.set(WCIFParse.getColorFromSchedule(self.wcif, venueVar.get(), roomVar.get())))
        getColorScheduleButton.grid(row=3, column=0, columnspan=2)
        bgColorLabel = tk.Label(window, text='Color:')
        bgColorLabel.grid(row=4, column=0, sticky='e')
        bgColorVariable = tk.StringVar()
        bgColorVariable.set(self.backgroundColor)
        bgColorButtonFrame = tk.Frame(window, highlightbackground='black', highlightthickness=1)
        bgColorButtonFrame.grid(row=4, column=1, sticky='w')
        bgColorButton = tk.Button(bgColorButtonFrame, text='', background=self.backgroundColor, relief=tk.FLAT, width=10)
        bgColorButton.configure(command=lambda: colorButtonCommand(bgColorButton, bgColorVariable, 'Stage color'))
        bgColorButton.pack()

        sampleUnclickedFrame = tk.Frame(window, highlightbackground='white', highlightthickness=2)
        sampleUnclickedFrame.grid(sticky='E', row=5, column=0)
        sampleUnclickedButton = tk.Button(sampleUnclickedFrame, text='Sample unclicked button', bg=self.backgroundColor, fg=self.textColor)
        sampleUnclickedButton.configure(relief=tk.RAISED)
        sampleUnclickedButton.pack()
        sampleClickedFrame = tk.Frame(window, highlightbackground='black', highlightthickness=2)
        sampleClickedFrame.grid(sticky='W', row=5, column=1)
        sampleClickedButton = tk.Button(sampleClickedFrame, text='Sample clicked button', bg=self.backgroundColor, fg=self.textColor)
        sampleClickedButton.configure(relief=tk.SUNKEN)
        sampleClickedButton.pack()

        bgColorVariable.trace_add('write', lambda var, index, mode:
                                  sampleUnclickedButton.configure(bg=bgColorVariable.get(), fg=getTextColorFromBackground(bgColorVariable.get())))
        bgColorVariable.trace_add('write', lambda var, index, mode:
                                  sampleClickedButton.configure(bg=bgColorVariable.get(), fg=getTextColorFromBackground(bgColorVariable.get())))
        bgColorVariable.trace_add('write', lambda var, index, mode: bgColorButton.configure(bg=bgColorVariable.get()))

        OKButton = tk.Button(window, text='OK', command=lambda:
                             self.updateWindowCloseButton(venueVar.get(), roomVar.get(), bgColorVariable.get(), window))
        OKButton.grid(row=6, column=0, columnspan=2)

        window.rowconfigure(0, pad=20)
        window.rowconfigure(1, pad=20)
        window.rowconfigure(2, pad=20)
        window.rowconfigure(3, pad=20)
        window.rowconfigure(4, pad=20)
        window.rowconfigure(5, pad=20)
        window.rowconfigure(6, pad=20)
        window.columnconfigure(0, pad=50)
        window.columnconfigure(1, pad=50)
        return window

    def copy(self):
        return Stage(self.root, self.wcif, self.backgroundColor, self.textColor, self.venue, self.room)
