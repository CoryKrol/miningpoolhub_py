from __future__ import print_function
from miningpoolhub_py import Pool

pool = Pool('ethereum')
profit_and_statistics = pool.get_dashboard()
print(profit_and_statistics)

# for number, coin in enumerate(profit_and_statistics, start=1):
#     print("{num}. {name} - {normalized_profit}".format(num=number,
#                                                        name=coin['coin_name'],
#                                                        normalized_profit=round(coin['normalized_profit'], 5)))
