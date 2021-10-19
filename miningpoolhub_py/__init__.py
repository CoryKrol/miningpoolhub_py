import os
from dotenv import load_dotenv
from .exceptions import APIKeyMissingError

load_dotenv()

__version__ = "0.1.10"
__author__ = 'Cory Krol'

API_KEY = os.environ.get('MPH_API_KEY', None)

from .pool import Pool
