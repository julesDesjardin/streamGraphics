import tkinter as tk
from TimeTower import TimeTower

root = tk.Tk()
root.title('Stream Time Tower')

timeTower = TimeTower.TimeTower(root)

root.mainloop()
