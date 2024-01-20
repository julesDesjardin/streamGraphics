def getActivities(wcif):
    activities = {}
    for venue in wcif['schedule']['venues']:
        for room in venue['rooms']:
            for activity in room['activities']:
                for childActivity in activity['childActivities']:
                    activities[childActivity['id']] = childActivity["activityCode"]
    return activities

def getCompetitors(wcif,activityId):
    competitors = []
    for i in range(0,len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor' and assignment['activityId'] == activityId:
                competitors.append(i)
    return competitors
