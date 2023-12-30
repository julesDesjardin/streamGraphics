import os, time

TIMEOUT = 5

exampleData = ['Tymon Kolasinski\nPR Single: 3.78\nPR Average: 4.86','Juliette Sebastien\nPR Single: 4.44\nPR Average: 6.27','Twan Dullemond\nPR Single: 4.38\nPR Average: 5.44','Sebastian Weyer\nPR Single: 4.32\nPR Average: 6.12']

def sendData(camera,id):
    timeStart = time.time()
    while f'changePending{camera}.txt' in os.listdir('.') and time.time() - timeStart < TIMEOUT:
        pass
    with open(f'./data{camera}.txt','w') as dataFile:
        dataFile.write(exampleData[id])
    with open(f'./changePending{camera}.txt','w') as changePendingFile:
        pass