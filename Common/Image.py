import tkinter as tk
from urllib.request import urlopen
import os
from PIL import Image, ImageTk


def getLocalImage(width, height, path):
    imageFull = Image.open(path)
    imageFull.thumbnail((width, height))
    return ImageTk.PhotoImage(imageFull)


def getInternetImage(width, height, url):
    imageFull = Image.open(urlopen(url))
    imageFull.thumbnail((width, height))
    return ImageTk.PhotoImage(imageFull)


def getAvatar(width, height, url):
    if url == 'local':
        image_path = f'{os.path.dirname(__file__)}/noAvatar.png'
        return getLocalImage(width, height, image_path)
    else:
        return getInternetImage(width, height, url)


def getFlag(height, country):
    width = 1000
    if country == 'local':
        # For debug/example purpose : use a local US flag to avoid losing time getting an actual flag from the internet
        image_path = f'{os.path.dirname(__file__)}/us.png'
        return getLocalImage(width, height, image_path)
    else:
        image_url = f'https://flagcdn.com/w320/{country.lower()}.png'
        return getInternetImage(width, height, image_url)
