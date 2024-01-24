import constants

def getActivities(wcif):
    activities = {}
    for venue in wcif['schedule']['venues']:
        for room in venue['rooms']:
            for activity in room['activities']:
                for childActivity in activity['childActivities']:
                    activities[childActivity['id']] = childActivity["activityCode"]
    return activities

def getRanking(wcif,competitor,event):
    for pb in wcif['persons'][competitor]['personalBests']:
        if pb['eventId'] == constants.EVENTS[event] and pb['type'] == constants.SEED_TYPE[constants.EVENTS[event]]:
            return pb['worldRanking']
    return constants.MAX_RANKING

def getAllCompetitorsRanked(wcif,event):
    competitors = []
    activities = getActivities(wcif)
    eventActivities = []
    for activity in activities:
        activitySplit = activities[activity].split('-')
        if activitySplit[0] == constants.EVENTS[event]:
            eventActivities.append(activity)

    for i in range(0,len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] in eventActivities:
                competitors.append(i)
    competitors.sort(key=lambda x:getRanking(wcif,x,event))
    return competitors

def getCompetitors(wcif,activityId,event):
    competitors = []
    competitorsRanked = getAllCompetitorsRanked(wcif,event)
    for i in range(0,len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] == activityId:
                competitors.append((i,competitorsRanked.index(i)))
    return competitors
