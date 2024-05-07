import tkinter as tk
import tkinter.filedialog
import cv2


def browse(entry):
    fileName = tkinter.filedialog.askopenfilename(initialdir='./')
    entry.delete(0, tk.END)
    entry.insert(0, fileName)


def loadVideo(videoFile, imageList):
    imageList.clear()
    vidcap = cv2.VideoCapture(videoFile)
    success, image = vidcap.read()
    (height, width, _) = image.shape
    while success:
        pngImage = cv2.imencode('.png', image)[1]
        imageFull = tk.PhotoImage(data=pngImage.tobytes())
        imageList.append(imageFull)
        success, image = vidcap.read()

    return (width, height)


def cleverInt(string):
    if string == '' or int(string) == 0:
        return 1
    else:
        return int(string)
