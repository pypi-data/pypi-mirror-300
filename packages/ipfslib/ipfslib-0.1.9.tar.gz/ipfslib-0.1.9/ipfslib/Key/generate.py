import json
import requests

# Generates new private key
def generate(api, key_name: str) -> str:
    params = {
        'arg': key_name,
    }
    response = requests.post('http://{endpoint}/api/v0/key/gen'.format(endpoint=api.endpoint), params=params)
    try:
        ipns_name = json.loads(response.text)["Id"]
    except KeyError:
        raise Exception(json.loads(response.text)['Message'])
    return ipns_name
