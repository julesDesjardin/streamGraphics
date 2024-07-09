import tkinter as tk
from urllib.request import urlopen
import os
from PIL import Image, ImageTk

storedImages = dict([])


def getLocalImage(width, height, path, keepImage):
    if keepImage:
        if path in storedImages:
            imageFull = storedImages[path].copy()
        else:
            imageFull = Image.open(path)
            storedImages[path] = imageFull.copy()
    else:
        imageFull = Image.open(path)
    imageFull.thumbnail((width, height))
    return ImageTk.PhotoImage(imageFull)


def getInternetImage(width, height, url, keepImage):
    if keepImage:
        if url in storedImages:
            imageFull = storedImages[url].copy()
        else:
            imageFull = Image.open(urlopen(url))
            storedImages[url] = imageFull.copy()
    else:
        imageFull = Image.open(urlopen(url))
    imageFull.thumbnail((width, height))
    return ImageTk.PhotoImage(imageFull)


def getAvatar(width, height, url):
    if url == 'local':
        image_path = f'{os.path.dirname(__file__)}/noAvatar.png'
        return getLocalImage(width, height, image_path, True)
    else:
        return getInternetImage(width, height, url, False)


def getFlag(height, country):
    width = 1000
    if country == 'local':
        # For debug/example purpose : use a local US flag to avoid losing time getting an actual flag from the internet
        image_path = f'{os.path.dirname(__file__)}/us.png'
        return getLocalImage(width, height, image_path, True)
    else:
        image_url = f'https://flagcdn.com/w320/{country.lower()}.png'
        return getInternetImage(width, height, image_url, True)
