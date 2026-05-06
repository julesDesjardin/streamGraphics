import tkinter as tk
from Cards import Cards
from TimeTower import TimeTower

root = tk.Tk()
root.title('Stream Display')

cards = Cards.Cards(root)
timeTower = TimeTower.TimeTower(root)

root.mainloop()
