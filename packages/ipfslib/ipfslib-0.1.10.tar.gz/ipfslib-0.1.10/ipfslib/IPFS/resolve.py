import json
import requests

# Resolve IPNS name
def resolve(api, ipns_name: str) -> None:
    params = {
        'arg': ipns_name
    }
    response = requests.post('http://{endpoint}/api/v0/name/resolve'.format(endpoint=api.endpoint), params=params)
    raw_json = response.text
    try:
        return json.loads(raw_json)['Path']
    except KeyError:
        raise Exception(json.loads(raw_json)['Message'])