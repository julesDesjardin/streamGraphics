import tkinter as tk
from urllib.request import urlopen
import os
from PIL import Image, ImageTk


def getFlag(width, height, country):
    if country == 'local':
        # For debug/example purpose : use a local US flag to avoid losing time getting an actual flag from the internet
        flagImageFull = Image.open(f'{os.path.dirname(__file__)}/us.png')
    else:
        image_url = f'https://flagcdn.com/w320/{country.lower()}.png'
        flagImageFull = Image.open(urlopen(image_url))
    flagImageFull.thumbnail((1000, height))
    return ImageTk.PhotoImage(flagImageFull)
