import json
import requests

# Remove file from ipfs (by CID)
def rem(api, content_hash: str, force: bool=True) -> None:
    params = {
        'arg': content_hash,
        'force': force
    }

    response = requests.post('http://{endpoint}/api/v0/block/rm'.format(endpoint=api.endpoint), params=params)