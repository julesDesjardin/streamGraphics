import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import json, urllib.request
import Stage
import constants

class Settings:

    BG_COLOR = '#F4ECE1'

    def __init__(self,root):
        self.root = root
        self.compId = ''
        self.wcif = {}
        self.rounds = {}
        self.groups = {}
        self.maxSeed = constants.MAX_SEED
        self.stages = []
    
    def updateCompIdCloseButton(self,compId,window):
        self.compId = compId
        try:
            self.reloadWCIF()
        except:
             tkinter.messagebox.showerror(title='Competition ID Error !', message='The WCIF was not found ! Please ensure that the competition ID is correct, you have access to the internet, and the WCA website is up')
        else:
            window.destroy()

    def updateCompId(self):
        compIdWindow = tk.Toplevel(self.root)
        compIdLabel = tk.Label(compIdWindow,text='Please enter competition ID to fetch the correct WCIF')
        compIdLabel.pack(padx=20,pady=5)
        compIdEntry = tk.Entry(compIdWindow,text=self.compId,width=50)
        compIdEntry.pack(padx=20,pady=5)
        compIdCloseButton = tk.Button(compIdWindow,text='Update and reload WCIF',command=lambda:self.updateCompIdCloseButton(compIdEntry.get(),compIdWindow))
        compIdCloseButton.pack(padx=20,pady=5)

    def reloadWCIF(self):
        jsonFile = urllib.request.urlopen(f'https://worldcubeassociation.org/api/v0/competitions/{self.compId}/wcif/public')
        self.wcif = json.loads(jsonFile.read())

    def updateMaxSeedCloseButton(self,maxSeed,window):
        try:
            self.maxSeed = int(maxSeed)
        except:
             tkinter.messagebox.showerror(title='Max Seed Error !', message='Error ! Please make sure the seed is a number')
        else:
            window.destroy()

    def updateMaxSeed(self):
        maxSeedWindow = tk.Toplevel(self.root)
        maxSeedLabel = tk.Label(maxSeedWindow,text='Please enter the maximum seed to be shown on stream')
        maxSeedLabel.pack(padx=20,pady=5)
        maxSeedEntry = tk.Entry(maxSeedWindow,text=self.maxSeed,width=20)
        maxSeedEntry.pack(padx=20,pady=5)
        maxSeedCloseButton = tk.Button(maxSeedWindow,text='Save max seed',command=lambda:self.updateMaxSeedCloseButton(maxSeedEntry.get(),maxSeedWindow))
        maxSeedCloseButton.pack(padx=20,pady=5)

    def updateStages(self):
        # TODO
        for stage in self.stages:
            stage.hideStage()
        stage = Stage.Stage(self.root, self.wcif, '#FFFFFF', '#000000')
        self.stages = [stage]
        stage.showStage()

    def showFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black',highlightthickness=1)
        settingsLabel = tk.Label(frame,text='Settings',bg=self.BG_COLOR)
        settingsLabel.grid(column=0,row=0)
        compIdButton = tk.Button(frame,text='Update competition ID',command=self.updateCompId)
        compIdButton.grid(column=0,row=1)
        reloadButton = tk.Button(frame,text='Reload WCIF',command=self.reloadWCIF)
        reloadButton.grid(column=0,row=2)
        maxSeedButton = tk.Button(frame,text='Change Max Seed',command=self.updateMaxSeed)
        maxSeedButton.grid(column=0,row=3)
        stagesButton = tk.Button(frame,text='Setup stages',command=self.updateStages)
        stagesButton.grid(column=0,row=4)
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)
        frame.rowconfigure(3, pad=20)
        frame.rowconfigure(4, pad=20)

