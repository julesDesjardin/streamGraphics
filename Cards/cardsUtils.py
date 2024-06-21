import tkinter as tk
import tkinter.filedialog
import cv2

CAMERAS_ROWS = 2
CAMERAS_COLS = 2
CAMERAS_COUNT = CAMERAS_ROWS * CAMERAS_COLS

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300
DEFAULT_FONT_FAMILY = 'Arial'
DEFAULT_FONT_SIZE = 20
DEFAULT_FLAG_WIDTH = 150
DEFAULT_FLAG_HEIGHT = 100
DEFAULT_FLAG_X = 100
DEFAULT_FLAG_Y = 100
DEFAULT_AVATAR_WIDTH = 100
DEFAULT_AVATAR_HEIGHT = 100
DEFAULT_AVATAR_X = 100
DEFAULT_AVATAR_Y = 200


def browse(entry):
    fileName = tkinter.filedialog.askopenfilename(initialdir='./')
    entry.delete(0, tk.END)
    entry.insert(0, fileName)


def loadVideo(videoFile, imageList):
    return loadVideoOrFirstFrame(videoFile, imageList, False)


def loadFirstFrame(videoFile):
    imageList = []
    (width, height) = loadVideoOrFirstFrame(videoFile, imageList, True)
    return (imageList[0], width, height)


def loadVideoOrFirstFrame(videoFile, imageList, firstFrameOnly):
    imageList.clear()
    vidcap = cv2.VideoCapture(videoFile)
    success, image = vidcap.read()
    (height, width, _) = image.shape
    while success:
        pngImage = cv2.imencode('.png', image)[1]
        imageFull = tk.PhotoImage(data=pngImage.tobytes())
        imageList.append(imageFull)
        success, image = vidcap.read()
        if firstFrameOnly:
            success = False

    return (width, height)
