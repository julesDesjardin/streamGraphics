import os, time

TIMEOUT = 5

def sendData(camera,id):
    timeStart = time.time()
    while f'changePending{camera}.txt' in os.listdir('.') and time.time() - timeStart < TIMEOUT:
        pass
    with open(f'./data{camera}.txt','w') as dataFile:
        dataFile.write(f'{id}')
    with open(f'./changePending{camera}.txt','w') as changePendingFile:
        pass