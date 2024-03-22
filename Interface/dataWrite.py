def resultToString(result):
    if result == 'DNF':
        return 'DNF'
    elif result >= 6000:
        return f"{int(result / 6000)}:{((result % 6000) / 100):05.2f}"
    return f"{((result % 6000) / 100):.2f}"

def sendCardData(bot,camera,data):
    bot.sendMessage(f'/cardData {camera} {data}')

def sendTimeTowerEvent(bot,event,round):
    bot.sendMessage(f'/timeTowerEvent {event} {round}')