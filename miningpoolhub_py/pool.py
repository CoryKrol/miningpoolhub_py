from . import session
from . import APIError


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
