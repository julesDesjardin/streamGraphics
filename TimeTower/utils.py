from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

MAX_RESULT = 10*60*100 # 10 min result

def getQueryResult(query):
    transport = AIOHTTPTransport(url="https://live.worldcubeassociation.org/api")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(gql(query))