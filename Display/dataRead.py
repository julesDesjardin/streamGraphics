import os

def readLoop(stopEvent, canvas,nameText,singleText,averageText):
    while True:
        if 'changePending.txt' in os.listdir('.'):
            with open('./data.txt','r') as dataFile:
                dataLine = dataFile.readline()
                dataList = dataLine.split(';')
            canvas.itemconfig(nameText, text=dataList[0])
            canvas.itemconfig(singleText, text='PR Single : ' + dataList[1])
            canvas.itemconfig(averageText, text='PR average : ' + dataList[2])
            os.remove('./changePending.txt')
        if stopEvent.is_set():
            break