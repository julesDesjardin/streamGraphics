import tkinter as tk
from Interface import Interface

root = tk.Tk()
root.title('Stream Interface')

interface = Interface.Interface(root)

root.mainloop()
