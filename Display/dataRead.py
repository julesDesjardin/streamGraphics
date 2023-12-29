import os

exampleData = ['Tymon Kolasinski;3.78;4.86','Juliette Sebastien;4.44;6.27','Twan Dullemond;4.38;5.44','Sebastian Weyer;4.32;6.12']

def readLoop(stopEvent,camera,canvas,nameText,singleText,averageText):
    while True:
        if f'changePending{camera}.txt' in os.listdir('.'):
            with open(f'./data{camera}.txt','r') as dataFile:
                id = dataFile.readline()
            dataLine = exampleData[int(id)]
            dataList = dataLine.split(';')
            canvas.itemconfig(nameText, text=dataList[0])
            canvas.itemconfig(singleText, text='PR Single : ' + dataList[1])
            canvas.itemconfig(averageText, text='PR Average : ' + dataList[2])
            os.remove(f'./changePending{camera}.txt')
        if stopEvent.is_set():
            break