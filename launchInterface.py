import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/Interface')
import tkinter as tk
import Interface

root = tk.Tk()
root.title('Stream Interface')

interface = Interface.Interface(root)

root.mainloop()
