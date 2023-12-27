import tkinter as tk
from tkinter import ttk
import dataWrite

def createButton(frame,name,id):
    print(id)
    return ttk.Button(frame,text=name,command=lambda:dataWrite.sendData(id))

root = tk.Tk()

main = tk.Frame(root)
main.pack()

ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")

personTest = ['Tymon Kolasinski','Juliette Sebastien','Twan Dullemond','Sebastian Weyer']
idTest = range(0,4)

buttons = []
for i in range(0,4):
    button = createButton(main,personTest[i],idTest[i])
    button.grid(column=0,row=i)
    
root.mainloop()