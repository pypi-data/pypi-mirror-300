import json
import requests
from typing import List

# Lists all IPNS keys
def list(api) -> List[dict]:
    response = requests.post('http://{endpoint}/api/v0/key/list'.format(endpoint=api.endpoint))
    raw_json = response.text
    try:
        return json.loads(raw_json)['Keys']
    except KeyError:
        raise Exception(json.loads(raw_json)['Message'])