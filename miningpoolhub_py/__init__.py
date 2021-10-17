import os
import requests

API_KEY = os.environ.get('MPH_API_KEY', None)


class APIKeyMissingError(Exception):
    pass


class APIError(Exception):
    pass


if API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an API key. See "
        "https://miningpoolhub.com/?page=account&action=edit "
        "for your Mining Pool Hub API Key"
    )
session = requests.Session()
session.params = {'api_key': API_KEY}

from .pool import Pool
