import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot


def resultToString(result):
    if result == 'DNF':
        return 'DNF'
    elif result >= 6000:
        return f"{int(result / 6000)}:{((result % 6000) / 100):05.2f}"
    return f"{((result % 6000) / 100):.2f}"


def sendCardData(bot, camera, country, name, avatar, text):
    fullData = [f'{camera}', country, name, avatar, text]
    bot.sendMessage('cardData', TelegramBot.DATA_SPLIT_SYMBOL.join(fullData))


def sendTimeTowerEvent(bot, event, round):
    bot.sendMessage('timeTowerEvent', f'{event} {round}')


def sendTimeTowerExpand(bot, id, enable):
    bot.sendMessage('timeTowerExpand', f'{id} {enable}')
