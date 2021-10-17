from miningpoolhub_py import Pool
from pytest import fixture
import vcr


@fixture
def dashboard_keys():
    return ['raw', 'personal', 'balance', 'balance_for_auto_exchange', 'balance_on_exchange', 'recent_credits',
            'coin_name', 'system', 'network']


@fixture
def hourly_hash_rate_keys():
    return ['id', 'username', 'hashrate']


@fixture
def mining_profit_and_statistics_keys():
    return ['coin_name', 'symbol', 'host', 'host_list', 'port', 'direct_mining_host', 'direct_mining_host_list',
            'direct_mining_algo_port', 'algo', 'normalized_profit', 'normalized_profit_amd', 'normalized_profit_nvidia',
            'profit', 'pool_hash', 'net_hash', 'difficulty', 'reward', 'last_block', 'time_since_last_block',
            'time_since_last_block_in_words', 'dovewallet_buy_price', 'bittrex_buy_price', 'poloniex_buy_price',
            'highest_buy_price', 'fee', 'workers']


@vcr.use_cassette('tests/vcr_cassettes/coin_name-dashboard.yml', filter_query_parameters=['api_key'])
def test_dashboard(dashboard_keys):
    """Tests an API call to get dashboard data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.dashboard()

    assert isinstance(response, dict)
    assert response['coin_name']['info']['currency'] == 'ETH', \
        'The coin name should be in the response'
    assert set(dashboard_keys).issubset(response.keys()), "All keys should be in the response"


@vcr.use_cassette('tests/vcr_cassettes/coin_name-hourly_hash_rate.yml', filter_query_parameters=['api_key'])
def test_hourly_hash_rate(hourly_hash_rate_keys):
    """Tests an API call to get hourly hash rate data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.hourly_hash_rate()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(hourly_hash_rate_keys).issubset(response[0].keys())


@vcr.use_cassette('tests/vcr_cassettes/coin_name-mining_profit_and_statistics.yml', filter_query_parameters=['api_key'])
def test_mining_profit_and_statistics(mining_profit_and_statistics_keys):
    """Tests an API call to get mining profit and statistics"""
    response = Pool.mining_profit_and_statistics()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(mining_profit_and_statistics_keys).issubset(response[0].keys())
