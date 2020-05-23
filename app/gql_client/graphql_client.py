from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

sample_transport=RequestsHTTPTransport(
    url='http://acad-overflow.herokuapp.com/v1/graphql',
    use_json=True,
    headers={
        "Content-type": "application/json",
    },
    verify=False
)

client = Client(
    retries=3,
    transport=sample_transport,
    fetch_schema_from_transport=True,
)

def process_entry_for_gql(sEntry):
    sEntry = repr(sEntry) # for '\n' character, converting into raw string
    sEntry = sEntry.replace("\"", "\\\"")
    return sEntry