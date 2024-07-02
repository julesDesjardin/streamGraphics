from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

##############################################################################
# DEBUG
##############################################################################

DEBUG_MODE_LOCAL_FLAG = False  # Default : False, put to True to use local USA flag as placeholder to reduce data usage
DEBUG_MODE_LOCALHOST_LIVE = False  # Default : False, put to True to use a local WCA Live for testing/developing

##############################################################################

DNF_ATTEMPT = 30 * 60 * 100  # 30 min, so an avg5/mo3 goes higher than 10 min
DNF_RESULT = 10 * 60 * 100  # 10 min

CRITERIA = dict([
    ('333', 'average'),
    ('222', 'average'),
    ('444', 'average'),
    ('555', 'average'),
    ('666', 'mean'),
    ('777', 'mean'),
    ('333bf', 'single'),
    ('333fm', 'mean'),
    ('333oh', 'average'),
    ('clock', 'average'),
    ('minx', 'average'),
    ('pyram', 'average'),
    ('skewb', 'average'),
    ('sq1', 'average'),
    ('444bf', 'single'),
    ('555bf', 'single'),
    ('333mbf', 'single'),
])

DEFAULT_BACKGROUND_COLOR = '#FFFFFF'
DEFAULT_BG_LOCAL_NAME = '#000000'
DEFAULT_BG_LOCAL_RESULT = '#555555'
DEFAULT_BG_FOREIGNER_NAME = '#444444'
DEFAULT_BG_FOREIGNER_RESULT = '#999999'
DEFAULT_WIDTH_RANKING = 50
DEFAULT_WIDTH_FLAG_RECTANGLE = 60
DEFAULT_HEIGHT_FLAG = 30
DEFAULT_WIDTH_NAME = 100
DEFAULT_WIDTH_FULL_NAME = 300
DEFAULT_WIDTH_COUNT = 50
DEFAULT_WIDTH_RESULT = 100
DEFAULT_WIDTH_FULL_RESULT = 300
DEFAULT_FONT_FAMILY = 'Arial'
DEFAULT_FONT_SIZE_BIG = 15
DEFAULT_FONT_SIZE_SMALL = 12
DEFAULT_HEIGHT = 50
DEFAULT_HEIGHT_SEPARATOR = 10
DEFAULT_COLOR_LOCAL_NAME = '#FFFFFF'
DEFAULT_COLOR_LOCAL_RESULT = '#FFFFFF'
DEFAULT_COLOR_FOREIGNER_NAME = '#FFFFFF'
DEFAULT_COLOR_FOREIGNER_RESULT = '#FFFFFF'
DEFAULT_MAX_NUMBER = 16
DEFAULT_DURATION_X = 1000
DEFAULT_DURATION_Y = 1000
DEFAULT_FPS_X = 50
DEFAULT_FPS_Y = 50

LAYOUT_MAX_WIDTH = 200
LAYOUT_MAX_HEIGHT = 200
LAYOUT_MAX_EXTENDED_WIDTH = 500
LAYOUT_MAX_FONT = 50
LAYOUT_CANVAS_WIDTH = 1000
LAYOUT_CANVAS_HEIGHT = 400


def getQueryResult(query):
    if (DEBUG_MODE_LOCALHOST_LIVE):
        url = 'http://localhost:4000/api'
    else:
        url = 'https://live.worldcubeassociation.org/api'
    transport = AIOHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(gql(query))


def getReadableResult(result):
    if (result >= DNF_RESULT):
        return 'DNF'
    output = ''
    if (result >= 6000):
        output = output + f'{int(result / 6000)}:'
    result = result % 6000
    output = output + f'{int(result / 100):02}.{result % 100:02}'
    return output


def getAllResults(results, criteria):
    outputArray = []
    minFound = False
    maxFound = False
    if len(results) <= 3 or criteria != 'average':
        minFound = True
        maxFound = True
    for result in results:
        if not maxFound and (result == max(results) or result >= DNF_RESULT):
            maxFound = True
            outputArray.append(f'({getReadableResult(result)})')
        elif not minFound and (result == min(results)):
            minFound = True
            outputArray.append(f'({getReadableResult(result)})')
        else:
            outputArray.append(f'{getReadableResult(result)}')
    return ' '.join(outputArray)
