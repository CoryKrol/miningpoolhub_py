import os
import requests
from dotenv import load_dotenv
from .exceptions import APIKeyMissingError

load_dotenv()

__version__ = "0.1.1"
__author__ = 'Cory Krol'

API_KEY = os.environ.get('MPH_API_KEY', None)

if API_KEY is None:
    raise APIKeyMissingError(
        "All methods require an API key. See "
        "https://miningpoolhub.com/?page=account&action=edit "
        "for your Mining Pool Hub API Key"
    )
session = requests.Session()
session.params = {'api_key': API_KEY}

from .pool import Pool
