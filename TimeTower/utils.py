from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

MAX_RESULT = 10*60*100 # 10 min result

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
    ('clk','average'),
    ('minx','average'),
    ('pyram','average'),
    ('skewb','average'),
    ('sq1','average'),
    ('444bf','single'),
    ('555bf','single'),
    ('333mbf','single'),
])

def getQueryResult(query):
    transport = AIOHTTPTransport(url="https://live.worldcubeassociation.org/api")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(gql(query))

def getReadableResult(result):
    output = ''
    if(result >= 6000):
        output = output + f'{int(result / 6000)}:'
    result = result % 6000
    output = output + f'{int(result / 100):02}.{result % 100:02}'
    return output