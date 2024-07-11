import tkinter as tk
import tkinter.filedialog
import cv2
from enum import Enum

CAMERAS_ROWS = 2
CAMERAS_COLS = 2
CAMERAS_COUNT = CAMERAS_ROWS * CAMERAS_COLS

DEFAULT_FPS = 25
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300
DEFAULT_FONT_FAMILY = 'Arial'
DEFAULT_FONT_SIZE = 20
DEFAULT_FONT_COLOR = '#000000'
DEFAULT_FLAG_WIDTH = 150
DEFAULT_FLAG_HEIGHT = 100
DEFAULT_FLAG_X = 100
DEFAULT_FLAG_Y = 100
DEFAULT_AVATAR_WIDTH = 100
DEFAULT_AVATAR_HEIGHT = 100
DEFAULT_AVATAR_X = 100
DEFAULT_AVATAR_Y = 200


class BackgroundState(Enum):
    EMPTY = 1
    INTRO = 2
    LOOP = 3
    OUTRO = 4


def browse(entry):
    fileName = tkinter.filedialog.askopenfilename(initialdir='./')
    entry.delete(0, tk.END)
    entry.insert(0, fileName)


def loadVideo(file, imageList):
    return loadVideoOrFirstFrame(file, imageList, False)


def loadFirstFrame(file):
    imageList = []
    (width, height) = loadVideoOrFirstFrame(file, imageList, True)
    return (imageList[0], width, height)


def loadVideoOrFirstFrame(file, imageList, firstFrameOnly):
    imageList.clear()
    try:
        vidcap = cv2.VideoCapture(file)
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
    except:
        image = cv2.imread(file)
        (height, width, _) = image.shape
        pngImage = cv2.imencode('.png', image)[1]
        imageFull = tk.PhotoImage(data=pngImage.tobytes())
        imageList.append(imageFull)
        return (width, height)
