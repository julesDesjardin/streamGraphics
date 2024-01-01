import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import json, urllib.request
import WCIFParse

class Settings:

    BG_COLOR = '#F4ECE1'

    def __init__(self,root):
        self.root = root
        self.compId = ''
        self.wcif = {}
    
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
        competitors = WCIFParse.getCompetitors(self.wcif)
        for personId in competitors['333-r3-g1']:
            print(self.wcif['persons'][personId]['name'])

    def showFrame(self):
        frame = tk.Frame(self.root, bg=self.BG_COLOR, highlightbackground='black',highlightthickness=1)
        settingsLabel = tk.Label(frame,text='Settings',bg=self.BG_COLOR)
        settingsLabel.grid(column=0,row=0)
        compIdButton = tk.Button(frame,text='Update competition ID',command=self.updateCompId)
        compIdButton.grid(column=0,row=1)
        reloadButton = tk.Button(frame,text='Reload WCIF',command=self.reloadWCIF)
        reloadButton.grid(column=0,row=2)
        frame.pack(side=tk.LEFT,fill=tk.BOTH)
        frame.columnconfigure(0, pad=20)
        frame.rowconfigure(0, pad=20)
        frame.rowconfigure(1, pad=20)
        frame.rowconfigure(2, pad=20)

