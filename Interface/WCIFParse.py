def getActivities(wcif):
    activities = {}
    for venue in wcif['schedule']['venues']:
        for room in venue['rooms']:
            for activity in room['activities']:
                activities[activity['id']] = activity["activityCode"]
                for childActivity in activity['childActivities']:
                    activities[childActivity['id']] = childActivity["activityCode"]
    return activities

def getCompetitors(wcif):
    competitors = {}
    activities = getActivities(wcif)
    for i in range(0,len(wcif['persons'])):
        for assignment in wcif['persons'][i]['assignments']:
            if assignment['assignmentCode'] == 'competitor':
                if activities[assignment['activityId']] not in competitors:
                    competitors[activities[assignment['activityId']]] = []
                competitors[activities[assignment['activityId']]].append(i)
    return competitors
