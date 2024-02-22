import tkinter as tk
from tkinter import ttk
import threading, queue
import dataRead

import sys
sys.path.append('.')
from Common import TelegramBot, Secrets

bot = TelegramBot.TelegramBot(Secrets.cardBotToken,Secrets.interfaceCardChannelId)

root = tk.Tk()
root.title('Stream Cards')

main = tk.Frame(root)
main.pack()

width = 1000
height = 3000
fontSize = 100

canvasLeft = tk.Canvas(main, width=width, height=height, background='#ff00ff')
canvasRight = tk.Canvas(main, width=width, height=height, background='#ff00ff')
textLeft = canvasLeft.create_text(100, 100, font=f'Helvetica {fontSize}', text='Bonjour', anchor='w')
textRight = canvasRight.create_text(100, 100, font=f'Helvetica {fontSize}', text='Bonjour', anchor='w')

queueLeft = queue.Queue()
queueRight = queue.Queue()

bot.setMessageHandler(['cardData'], lambda message:dataRead.botCallback(message, queueLeft, queueRight))
threadBot = threading.Thread(target=bot.startPolling)
threadBot.start()

def startButtonAction(button):
    dataRead.checkBothQueues(root, queueLeft, queueRight, canvasLeft, canvasRight, textLeft, textRight)
    button.pack_forget()

startButton = tk.Button(main, text='Start', command=lambda:startButtonAction(startButton))
startButton.pack(side=tk.TOP)
canvasLeft.pack(side=tk.LEFT)
canvasRight.pack(side=tk.LEFT)

root.mainloop()
threadBot.join()