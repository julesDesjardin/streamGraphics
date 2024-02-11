import tkinter as tk
from tkinter import ttk
import constants, WCIFParse

class Stage:

    def __init__(self,root,wcif,backgroundColor,textColor):
        self.root = root
        self.wcif = wcif
        self.backgroundColor = backgroundColor
        self.textColor = textColor
        self.frame = tk.Frame(self.root, bg=self.backgroundColor, highlightbackground='black',highlightthickness=1, padx=50, pady=20)
        self.eventLabel = tk.Label(self.frame,text='Event:', bg=self.backgroundColor, fg=self.textColor)
        self.eventLabel.grid(column=0,row=0,sticky=tk.E)
        self.eventVar = tk.StringVar()
        self.eventMenu = ttk.OptionMenu(self.frame,self.eventVar,list(constants.EVENTS.keys())[0],*list(constants.EVENTS.keys()))
        self.eventMenu.grid(column=1,row=0,sticky=tk.W)
        self.roundLabel = tk.Label(self.frame,text='Round:', bg=self.backgroundColor, fg=self.textColor)
        self.roundLabel.grid(column=2,row=0,sticky=tk.E)
        self.roundVar = tk.StringVar()
        self.roundMenu = ttk.OptionMenu(self.frame,self.roundVar)
        self.roundMenu.grid(column=3,row=0,sticky=tk.W)
        self.groupLabel = tk.Label(self.frame,text='Group:', bg=self.backgroundColor, fg=self.textColor)
        self.groupLabel.grid(column=4,row=0,sticky=tk.E)
        self.groupVar = tk.StringVar()
        self.groupMenu = ttk.OptionMenu(self.frame,self.groupVar)
        self.groupMenu.grid(column=5,row=0,sticky=tk.W)

        self.roundVar.trace_add('write',lambda var,index,mode :self.updateGroups())
        self.eventVar.trace_add('write',lambda var,index,mode :self.updateRounds())


    def updateGroups(self):
        activities = WCIFParse.getActivities(self.wcif)
        maxGroup = 0
        for activity in activities:
            activitySplit = activities[activity].split('-')
            if activitySplit[0] == constants.EVENTS[self.eventVar.get()] and activitySplit[1] == f'r{self.roundVar.get()}':
                maxGroup = max(maxGroup,int(activitySplit[2][1:]))
        menu = self.groupMenu["menu"]
        menu.delete(0, "end")
        if maxGroup > 0:
            for i in range(1,maxGroup+1):
                menu.add_command(label=f'{i}',command=lambda value=f'{i}': self.groupVar.set(value))
            self.groupVar.set(1)
        else:
            menu.add_command(label='No group',command=lambda value=0:self.roundVar.set(value))
            self.groupVar.set(0)

    def updateRounds(self):
        activities = WCIFParse.getActivities(self.wcif)
        maxRound = 0
        for activity in activities:
            activitySplit = activities[activity].split('-')
            if activitySplit[0] == constants.EVENTS[self.eventVar.get()]:
                maxRound = max(maxRound,int(activitySplit[1][1:]))
        menu = self.roundMenu["menu"]
        menu.delete(0, "end")
        if maxRound > 0:
            for i in range(1,maxRound+1):
                menu.add_command(label=f'{i}',command=lambda value=f'{i}': self.roundVar.set(value))
            self.roundVar.set(1)
        else:
            menu.add_command(label='No round',command=lambda value=0:self.roundVar.set(value))
            self.roundVar.set(0)

    def hideStage(self):
        self.frame.pack_forget()

    def showStage(self):
        self.frame.pack()

    def setEvent(self,event):
        self.eventVar.set(event)

    def setRound(self,round):
        self.roundVar.set(round)
