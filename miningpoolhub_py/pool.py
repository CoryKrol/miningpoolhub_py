from requests import Session
from requests import HTTPError
from . import API_KEY

from .exceptions import APIError
from .urls import Urls


class Pool(object):
    __session = None
    __api_key = None

    def __init__(self, coin_name, api_key=API_KEY):
        self.__api_key = api_key
        self.coin_name = coin_name
        self.urls = Urls()

    @property
    def session(self):
        if self.__session is None:
            self.__session = Session()
            self.__session.params = {'api_key': self.__api_key}

        return self.__session

    @session.setter
    def session(self, value):
        raise AttributeError('Setting \'session\' attribute is prohibited.')

    def __to_json(self, response):
        """Private method to call json method on response object"""
        return response.json()

    def __get_data(self, url):
        """Private method to make a GET request to the URL"""
        try:
            response = self.session.get(url)

            # raises if the status code is an error - 4xx, 5xx
            response.raise_for_status()

            return self.__to_json(response)
        except HTTPError as e:
            pass

    def get_dashboard(self):
        """Load a user's dashboard data for a pool: hash rate, share rate, balance, recent credits"""
        return self.__get_data(self.urls.get_dashboard_data_url(pool=self.coin_name))['getdashboarddata']['data']

    def get_hourly_hash_rate(self):
        """Get the average hash rate each hour for the last 24 hours, total and by worker"""
        return self.__get_data(self.urls.get_hourly_hash_rates_url(pool=self.coin_name))['gethourlyhashrates']['data']['mine']

    def public(self):
        """Fetch public pool statistics, no authentication required"""
        return self.__get_data(self.urls.public_url(self.coin_name))

    def get_auto_switching_and_profits_statistics(self):
        """Get auto switching information"""
        path = self.urls.get_auto_switching_and_profits_statistics_url()
        response = self.__get_data(path)
        if response['success'] is not True:
            raise APIError('Call failed')

        return response['return']

    def get_mining_profit_and_statistics(self):
        """Get mining profits statistics"""
        path = self.urls.get_mining_profit_and_statistics_url()
        response = self.__get_data(path)
        if response['success'] is not True:
            raise APIError('Call failed')

        return response['return']

    def get_user_all_balances(self):
        """Get all currency balances for a user"""
        return self.__get_data(self.urls.get_user_all_balances_url())['getuserallbalances']['data']
