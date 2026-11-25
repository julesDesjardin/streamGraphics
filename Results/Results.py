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
    prSingle: int
    prAverage: int
    results: list[SingleResult] = field(default_factory=list)
    resultUpdated: bool = False
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

        # Get competitor's seeds for ranking later + get competitors' id in the wcif (not registrant id)
        competitorsRanked = WCIFParse.getAllCompetitorsRanked(wcif, event)
        competitorsRank = dict([])
        competitorsId = dict([])
        for (i, competitor) in enumerate(competitorsRanked):
            competitorsRank[WCIFParse.getRegistrantId(wcif, competitor)] = i + 1
            competitorsId[WCIFParse.getRegistrantId(wcif, competitor)] = competitor

        # Get all competitors: first get their registrationId
        self.requestUrl = f"v1/competitions/{self.compId}/live/rounds/{f'{utils.EVENTS[self.event]}-r{self.round}'}"
        requestCompetitors = utils.getRequestResult(self.requestUrl)['competitors']
        self.allCompetitors = []
        for competitor in requestCompetitors:
            self.allCompetitors.append(Competitor(
                id=competitor['registrant_id'], registrationId=competitor['id'], name=utils.cleanName(competitor['name']), country=competitor['country_iso2'],
                prSingle=WCIFParse.getPb(wcif, competitorsId[competitor['registrant_id']], event, 'single'),
                prAverage=WCIFParse.getPb(wcif, competitorsId[competitor['registrant_id']], event, 'average')
            ))

        self.allCompetitors.sort(key=lambda x: competitorsRank[x.id])

        # Get competitors in the group
        self.competitorsInGroup = []
        for (venue, room) in zip(venues, rooms):
            for competitor in WCIFParse.getCompetitors(wcif, WCIFParse.getActivityId(wcif, venue, room, event, round, group), event):
                self.competitorsInGroup.append(WCIFParse.getRegistrantId(wcif, competitor[0]))

        self.stopEvent = threading.Event()
        self.resultsThread = threading.Thread(target=self.fullLoop, daemon=True)
        self.resultsThread.start()

    def updateResults(self):
        for competitor in self.allCompetitors:
            competitor.resultUpdated = False

        try:
            data = utils.getRequestResult(self.requestUrl)
            for result in data['results']:
                for competitor in self.allCompetitors:
                    if competitor.registrationId == result['registration_id']:
                        for (i, attempt) in enumerate(result['attempts']):
                            if i >= len(competitor.results):
                                competitor.results.append(SingleResult(result=attempt['value'], tag=''))
                                competitor.resultUpdated = True
                            elif competitor.results[i].result != attempt['value']:
                                competitor.results[i] = SingleResult(result=attempt['value'], tag='')
                                competitor.resultUpdated = True
        except Exception as e:
            print(f"Error fetching results: {e}")

    def fullLoop(self):
        while (not self.stopEvent.is_set()):
            self.updateResults()
            print(self.allCompetitors)
            self.stopEvent.wait(self.reloadPeriod / 1000)
