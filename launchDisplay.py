import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/Cards')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/TimeTower')
import tkinter as tk
import Cards
import TimeTower

root = tk.Tk()
root.title('Stream Display')

Cards = Cards.Cards(root)
timeTower = TimeTower.TimeTower(root)

root.mainloop()
