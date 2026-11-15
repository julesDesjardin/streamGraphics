import threading
import requests

from Interface import interfaceUtils


class Results:
    def __init__(self, wcif, compId, event, round, group, reloadPeriod):
        self.wcif = wcif
        self.compId = compId
        self.event = event
        self.round = round
        self.group = group
        self.reloadPeriod = reloadPeriod

        self.stopEvent = threading.Event()
        self.resultsThread = threading.Thread(target=self.updateResults, daemon=True)
        self.resultsThread.start()

    def updateResults(self):
        while (not self.stopEvent.is_set()):
            try:
                response = requests.get(
                    f'https://www.worldcubeassociation.org/api/v1/competitions/{self.compId}/live/rounds/{f"{interfaceUtils.EVENTS[self.event]}-r{self.round}"}', timeout=10)
                response.raise_for_status()
                data = response.json()
                print(data['results'][0])
                for competitor in data['competitors']:
                    if data['results'][0]['registration_id'] == competitor['id']:
                        print(competitor)
                return
            except Exception as e:
                print(f"Error fetching results: {e}")
            self.stopEvent.wait(self.reloadPeriod / 1000)
