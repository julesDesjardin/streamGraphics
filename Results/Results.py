import threading
from dataclasses import dataclass, field
import requests

from Common import utils, WCIFParse


@dataclass
class SingleResult:
    result: int
    tag: str
    best: bool | None = None
    worst: bool | None = None


@dataclass
class Competitor:
    id: int
    registrationId: int
    name: str
    country: str
    results: list[SingleResult] = field(default_factory=list)
    bpa: SingleResult | None = None
    wpa: SingleResult | None = None


class Results:
    def __init__(self, wcif, compId, venues, rooms, event, round, group, reloadPeriod, numberRanked, numberFocused):
        self.wcif = wcif
        self.compId = compId
        self.venues = venues
        self.rooms = rooms
        self.event = event
        self.round = round
        self.group = group
        self.reloadPeriod = reloadPeriod
        self.numberRanked = numberRanked
        self.numberFocused = numberFocused

        # Get competitor's seeds for ranking later
        competitorsRanked = WCIFParse.getAllCompetitorsRanked(wcif, event)
        competitorsRank = dict([])
        for (i, competitor) in enumerate(competitorsRanked):
            competitorsRank[WCIFParse.getRegistrantId(wcif, competitor)] = i + 1
        print(competitorsRank)

        # Get all competitors: first get their registrationId
        self.requestUrl = f"https://www.worldcubeassociation.org/api/v1/competitions/{self.compId}/live/rounds/{f'{utils.EVENTS[self.event]}-r{self.round}'}"
        requestCompetitors = utils.getRequestResult(self.requestUrl)['competitors']
        self.allCompetitors = []
        for competitor in requestCompetitors:
            self.allCompetitors.append(Competitor(
                id=competitor['registrant_id'], registrationId=competitor['id'], name=utils.cleanName(competitor['name']), country=competitor['country_iso2']))

        self.allCompetitors.sort(key=lambda x: competitorsRank[x.id])

        # Get competitors in the group
        self.competitorsInGroup = []
        for (venue, room) in zip(venues, rooms):
            for competitor in WCIFParse.getCompetitors(wcif, WCIFParse.getActivityId(wcif, venue, room, event, round, group), event):
                self.competitorsInGroup.append(WCIFParse.getRegistrantId(wcif, competitor[0]))

        self.stopEvent = threading.Event()
        self.resultsThread = threading.Thread(target=self.updateResults, daemon=True)
        self.resultsThread.start()

    def updateResults(self):
        while (not self.stopEvent.is_set()):
            try:
                data = utils.getRequestResult(self.requestUrl)
                print(data['results'][0])
                for competitor in data['competitors']:
                    if data['results'][0]['registration_id'] == competitor['id']:
                        print(competitor)
                return
            except Exception as e:
                print(f"Error fetching results: {e}")
            self.stopEvent.wait(self.reloadPeriod / 1000)
