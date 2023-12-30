import os

def readLoop(stopEvent,camera,canvas,texts):
    while True:
        if f'changePending{camera}.txt' in os.listdir('.'):
            for textLine in texts:
                canvas.itemconfig(textLine, text='')
            with open(f'./data{camera}.txt','r') as dataFile:
                counter = 0
                for line in dataFile.readlines():
                    canvas.itemconfig(texts[counter], text=line)
                    counter = counter + 1
            os.remove(f'./changePending{camera}.txt')
        if stopEvent.is_set():
            break