import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/Cards')
import tkinter as tk
import Cards

root = tk.Tk()
root.title('Stream Cards')

cards = Cards.Cards(root)

root.mainloop()
