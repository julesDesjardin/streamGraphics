import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/TimeTower')
import tkinter as tk
import TimeTower

root = tk.Tk()
root.title('Stream Time Tower')

timeTower = TimeTower.TimeTower(root)

root.mainloop()
