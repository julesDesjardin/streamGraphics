def checkQueue(root, queue, canvas, text):
    while True:
        try:
            data = queue.get(timeout=0.1)
        except:
            break
        canvas.itemconfig(text, text=data)
    root.after(1000, lambda:checkQueue(root, queue, canvas, text))

def checkBothQueues(root, queueLeft, queueRight, canvasLeft, canvasRight, textLeft, textRight):
    checkQueue(root, queueLeft, canvasLeft, textLeft)
    checkQueue(root, queueRight, canvasRight, textRight)

def botCallback(message, queueLeft, queueRight):
    fullMessage = message.text.removeprefix('/cardData ')
    camera = fullMessage[0]
    data = fullMessage[2:]
    print('Start put')
    if camera == '0':
        queueLeft.put(data)
    elif camera == '1':
        queueRight.put(data)
    else:
        print('Camera unknown!')
    print('OK put')