import utils


def getVenueName(wcif, venueId):
    for venue in wcif['schedule']['venues']:
        if venue['id'] == venueId:
            return venue['name']
    return 'VENUE NOT FOUND'


def getRoomName(wcif, venueId, roomId):
    for venue in wcif['schedule']['venues']:
        if venue['id'] == venueId:
            for room in venue['rooms']:
                if room['id'] == roomId:
                    return room['name']
    return 'ROOM NOT FOUND'


def getVenueId(wcif, venueName):
    for venue in wcif['schedule']['venues']:
        if venue['name'] == venueName:
            return venue['id']
    return 'VENUE NOT FOUND'


def getRoomId(wcif, venueId, roomName):
    for venue in wcif['schedule']['venues']:
        if venue['id'] == venueId:
            for room in venue['rooms']:
                if room['name'] == roomName:
                    return room['id']
    return 'ROOM NOT FOUND'


def getRoomColor(wcif, venueId, roomId):
    for venue in wcif['schedule']['venues']:
        if venue['id'] == venueId:
            for room in venue['rooms']:
                if room['id'] == roomId:
                    return room['color']
    return 'ROOM NOT FOUND'


def getVenues(wcif):
    result = []
    for venue in wcif['schedule']['venues']:
        result.append(venue['name'])
    return result


def getRooms(wcif, venueId):
    result = []
    for venue in wcif['schedule']['venues']:
        if venue['id'] == venueId:
            for room in venue['rooms']:
                result.append(room['name'])
    return result


def getActivities(wcif, venueId, roomId):
    activities = {}
    for venue in wcif['schedule']['venues']:
        if venueId == -1 or venue['id'] == venueId:
            for room in venue['rooms']:
                if roomId == -1 or room['id'] == roomId:
                    for activity in room['activities']:
                        for childActivity in activity['childActivities']:
                            activities[childActivity['id']] = childActivity["activityCode"]
    return activities


def getActivityId(wcif, venueId, roomId, event, round, group):
    activities = getActivities(wcif, venueId, roomId)
    for activity in activities:
        if activities[activity] == f'{utils.EVENTS[event]}-r{round}-g{group}':
            return activity


def getPb(wcif, competitor, event, singleOrAverage):
    for pb in wcif['persons'][competitor]['personalBests']:
        if pb['eventId'] == utils.EVENTS[event] and pb['type'] == singleOrAverage:
            return pb['best']
    return 'DNF'


def getRanking(wcif, competitor, event, singleOrAverage, scale):
    for pb in wcif['persons'][competitor]['personalBests']:
        if pb['eventId'] == utils.EVENTS[event] and pb['type'] == singleOrAverage:
            return pb[f'{scale}Ranking']
    return utils.MAX_RANKING


def getRoundResult(wcif, competitor, event, round, singleOrAverage):
    if round is None:
        return 'DNF'
    registrantId = wcif['persons'][competitor]['registrantId']
    for wcifEvent in wcif['events']:
        if (wcifEvent['id'] == utils.EVENTS[event]):
            for wcifRound in wcifEvent['rounds']:
                if (wcifRound['id'] == f'{utils.EVENTS[event]}-r{round}'):
                    for result in wcifRound['results']:
                        if (result['personId'] == registrantId):
                            if (singleOrAverage == 'single'):
                                return result['best']
                            return result['average']
    return 'DNF'


def getRoundRank(wcif, competitor, event, round):
    if round is None:
        return None
    registrantId = wcif['persons'][competitor]['registrantId']
    for wcifEvent in wcif['events']:
        if (wcifEvent['id'] == utils.EVENTS[event]):
            for wcifRound in wcifEvent['rounds']:
                if (wcifRound['id'] == f'{utils.EVENTS[event]}-r{round}'):
                    for result in wcifRound['results']:
                        if (result['personId'] == registrantId):
                            return result['ranking']
    return utils.MAX_RANKING


def getAllCompetitorsRanked(wcif, event):
    competitors = []
    activities = getActivities(wcif, -1, -1)
    eventActivities = []
    for activity in activities:
        activitySplit = activities[activity].split('-')
        if activitySplit[0] == utils.EVENTS[event] and activitySplit[1] == 'r1':  # Only count R1 for seeding
            eventActivities.append(activity)

    for i in range(0, len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] in eventActivities:
                competitors.append(i)
    competitors.sort(key=lambda x: getRanking(wcif, x, event, utils.SEED_TYPE[utils.EVENTS[event]], 'world'))
    return competitors


def getCompetitors(wcif, activityId, event):
    competitors = []
    competitorsRanked = getAllCompetitorsRanked(wcif, event)
    for i in range(0, len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] == activityId:
                competitors.append((i, competitorsRanked.index(i) + 1))  # + 1 because first seed is 1 and first index is 0
    return competitors


def getRegistrantId(wcif, competitor):
    return wcif['persons'][competitor]['registrantId']


def getCountry(wcif, competitor):
    return wcif['persons'][competitor]['countryIso2']


def getWCAID(wcif, competitor):
    return wcif['persons'][competitor]['wcaId']


def getCompetitorName(wcif, competitor):
    return wcif['persons'][competitor]['name']


def getAvatar(wcif, competitor):
    return wcif['persons'][competitor]['avatar']['url']
