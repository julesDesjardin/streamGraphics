import os

def readLoop(canvas,nameText,singleText,averageText):
    while True:
        if 'changePending.txt' in os.listdir('.'):
            with open('./data.txt','r') as dataFile:
                dataLine = dataFile.readline()
                print(dataLine)
                dataList = dataLine.split(';')
                print(dataList)
            canvas.itemconfig(nameText, text=dataList[0])
            canvas.itemconfig(singleText, text='PR Single : ' + dataList[1])
            canvas.itemconfig(averageText, text='PR average : ' + dataList[2])
            os.remove('./changePending.txt')