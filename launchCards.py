import tkinter as tk
from Cards import Cards

root = tk.Tk()
root.title('Stream Cards')

cards = Cards.Cards(root)

root.mainloop()
