from __future__ import print_function

from . import session
from .exceptions import APIError
from .urls import Urls


class Pool(object):
    def __init__(self, coin_name):
        self.coin_name = coin_name
        self.urls = Urls()

    def dashboard(self):
        return session.get(self.urls.get_dashboard_data_url(pool=self.coin_name)).json()['getdashboarddata']['data']

    def hourly_hash_rate(self):
        return session.get(self.urls.get_hourly_hash_rates_url(pool=self.coin_name)).json()['gethourlyhashrates']['data']['mine']

    def mining_profit_and_statistics(self):
        path = self.urls.get_mining_profit_and_statistics_url()
        response = session.get(path).json()
        if response['success'] is not True:
            raise APIError('Call failed')

        return response['return']


if __name__ == "__main__":
    profit_and_statistics = Pool.get_mining_profit_and_statistics_url()

    for number, coin in enumerate(profit_and_statistics, start=1):
        print("{num}. {name} - {normalized_profit}".format(num=number,
                                                           name=coin['coin_name'],
                                                           normalized_profit=round(coin['normalized_profit'], 5)))
