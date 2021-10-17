from __future__ import print_function
from miningpoolhub_py import Pool

profit_and_statistics = Pool.mining_profit_and_statistics()

for number, coin in enumerate(profit_and_statistics, start=1):
    print("{num}. {name} - {normalized_profit}".format(num=number,
                                                       name=coin['coin_name'],
                                                       normalized_profit=round(coin['normalized_profit'], 5)))
