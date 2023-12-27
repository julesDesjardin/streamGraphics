import os

def sendData(id):
    print('start')
    while 'changePending.txt' in os.listdir('.'):
        pass
    print('ok')
    exampleData = ['Tymon Kolasinski;3.78;4.86','Juliette Sebastien;4.44;6.27','Twan Dullemond;4.38;5.44','Sebastian Weyer;4.32;6.12']
    with open('./data.txt','w') as dataFile:
        dataFile.write(exampleData[int(id)])
    with open('./changePending.txt','w') as changePendingFile:
        pass