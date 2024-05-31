import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Common import TelegramBot


def sendCardData(bot, camera, country, name, avatar, text, immediate):
    fullData = [f'{camera}', country, name, avatar, text]
    if immediate:
        command = ['cardData', TelegramBot.DATA_SPLIT_SYMBOL.join(fullData)]
        bot.sendSimpleMessage('/streamCommand \n' + TelegramBot.COMMAND_SYMBOL.join(command))
    else:
        bot.sendMessage('cardData', TelegramBot.DATA_SPLIT_SYMBOL.join(fullData))


def sendTimeTowerEvent(bot, event, round):
    bot.sendMessage('timeTowerEvent', f'{event} {round}')


def sendTimeTowerExpand(bot, id, enable):
    bot.sendMessage('timeTowerExpand', f'{id} {enable}')
