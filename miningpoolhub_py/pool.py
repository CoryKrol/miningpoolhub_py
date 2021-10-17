from __future__ import print_function

from . import session
from .exceptions import APIError


class Pool(object):
    def __init__(self, coin_name):
        self.coin_name = coin_name

    def dashboard(self):
        path = 'https://{}.miningpoolhub.com/index.php?page=api&action=getdashboarddata'.format(self.coin_name)
        return session.get(path).json()['getdashboarddata']['data']

    def hourly_hash_rate(self):
        path = 'https://{}.miningpoolhub.com/index.php?page=api&action=gethourlyhashrates'.format(self.coin_name)
        return session.get(path).json()['gethourlyhashrates']['data']['mine']

    @staticmethod
    def mining_profit_and_statistics():
        path = 'https://miningpoolhub.com/index.php?page=api&action=getminingandprofitsstatistics'
        response = session.get(path).json()
        if response['success'] is not True:
            raise APIError('Call failed')

        return response['return']


if __name__ == "__main__":
    profit_and_statistics = Pool.mining_profit_and_statistics()

    for number, coin in enumerate(profit_and_statistics, start=1):
        print("{num}. {name} - {normalized_profit}".format(num=number,
                                                           name=coin['coin_name'],
                                                           normalized_profit=round(coin['normalized_profit'], 5)))