def resultToString(result):
    if result == 'DNF':
        return 'DNF'
    elif result >= 6000:
        return f"{int(result / 6000)}:{((result % 6000) / 100):05.2f}"
    return f"{((result % 6000) / 100):.2f}"


def sendCardData(bot, camera, data):
    bot.sendMessage('cardData', f'{camera} {data}')


def sendTimeTowerEvent(bot, event, round):
    bot.sendMessage('timeTowerEvent', f'{event} {round}')


def sendTimeTowerExpand(bot, id, enable):
    bot.sendMessage('timeTowerExpand', f'{id} {enable}')
