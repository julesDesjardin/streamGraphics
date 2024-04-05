from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

##############################################################################
# DEBUG
##############################################################################

DEBUG_MODE_LOCAL_FLAG = False # Default : False, put to True to use local USA flag as placeholder to reduce data usage
DEBUG_MODE_LOCALHOST_LIVE = False # Default : False, put to True to use a local WCA Live for testing/developing

##############################################################################

DNF_ATTEMPT = 30*60*100 # 30 min, so an avg5/mo3 goes higher than 10 min
DNF_RESULT = 10*60*100 # 10 min

CRITERIA = dict([
    ('333','average'),
    ('222','average'),
    ('444','average'),
    ('555','average'),
    ('666','mean'),
    ('777','mean'),
    ('333bf','single'),
    ('333fm','mean'),
    ('333oh','average'),
    ('clock','average'),
    ('minx','average'),
    ('pyram','average'),
    ('skewb','average'),
    ('sq1','average'),
    ('444bf','single'),
    ('555bf','single'),
    ('333mbf','single'),
])

def getQueryResult(query):
    if(DEBUG_MODE_LOCALHOST_LIVE):
        url = 'http://localhost:4000/api'
    else:
        url = 'https://live.worldcubeassociation.org/api'
    transport = AIOHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(gql(query))

def getReadableResult(result):
    if(result >= DNF_RESULT):
        return 'DNF'
    output = ''
    if(result >= 6000):
        output = output + f'{int(result / 6000)}:'
    result = result % 6000
    output = output + f'{int(result / 100):02}.{result % 100:02}'
    return output