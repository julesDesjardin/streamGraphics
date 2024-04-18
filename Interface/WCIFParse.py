import constants

def getActivities(wcif,venueId,roomId):
    activities = {}
    for venue in wcif['schedule']['venues']:
        if venueId == -1 or venue['id'] == venueId:
            for room in venue['rooms']:
                if roomId == -1 or room['id'] == roomId:
                    for activity in room['activities']:
                        for childActivity in activity['childActivities']:
                            activities[childActivity['id']] = childActivity["activityCode"]
    return activities

def getPb(wcif,competitor,event,singleOrAverage):
    for pb in wcif['persons'][competitor]['personalBests']:
        if pb['eventId'] == constants.EVENTS[event] and pb['type'] == singleOrAverage:
            return pb['best']
    return 'DNF'

def getRanking(wcif,competitor,event,singleOrAverage,scale):
    for pb in wcif['persons'][competitor]['personalBests']:
        if pb['eventId'] == constants.EVENTS[event] and pb['type'] == singleOrAverage:
            return pb[f'{scale}Ranking']
    return constants.MAX_RANKING

def getRoundResult(wcif,competitor,event,round,singleOrAverage):
    if round is None:
        return 'DNF'
    registrantId = wcif['persons'][competitor]['registrantId']
    for wcifEvent in wcif['events']:
        if(wcifEvent['id'] == constants.EVENTS[event]):
            for wcifRound in wcifEvent['rounds']:
                if(wcifRound['id'] == f'{constants.EVENTS[event]}-r{round}'):
                    for result in wcifRound['results']:
                        if(result['personId'] == registrantId):
                            if(singleOrAverage == 'single'):
                                return result['best']
                            return result['average']
    return 'DNF'

def getRoundRank(wcif,competitor,event,round):
    if round is None:
        return None
    registrantId = wcif['persons'][competitor]['registrantId']
    for wcifEvent in wcif['events']:
        if(wcifEvent['id'] == constants.EVENTS[event]):
            for wcifRound in wcifEvent['rounds']:
                if(wcifRound['id'] == f'{constants.EVENTS[event]}-r{round}'):
                    for result in wcifRound['results']:
                        if(result['personId'] == registrantId):
                            return result['ranking']
    return constants.MAX_RANKING

def getAllCompetitorsRanked(wcif,event):
    competitors = []
    activities = getActivities(wcif, -1, -1)
    eventActivities = []
    for activity in activities:
        activitySplit = activities[activity].split('-')
        if activitySplit[0] == constants.EVENTS[event] and activitySplit[1] == 'r1': # Only count R1 for seeding
            eventActivities.append(activity)

    for i in range(0,len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] in eventActivities:
                competitors.append(i)
    competitors.sort(key=lambda x:getRanking(wcif,x,event,constants.SEED_TYPE[constants.EVENTS[event]],'world'))
    return competitors

def getCompetitors(wcif,activityId,event):
    competitors = []
    competitorsRanked = getAllCompetitorsRanked(wcif,event)
    for i in range(0,len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] == activityId:
                competitors.append((i,competitorsRanked.index(i) + 1)) # + 1 because first seed is 1 and first index is 0
    return competitors
