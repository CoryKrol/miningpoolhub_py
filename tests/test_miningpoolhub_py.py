from miningpoolhub_py import Pool
from pytest import fixture
import vcr


@fixture
def get_block_stats_keys():
    return ['Total', 'TotalValid', 'TotalOrphan', 'TotalDifficulty', 'TotalShares', 'TotalEstimatedShares',
            'TotalAmount', '1HourTotal', '1HourValid', '1HourOrphan', '1HourDifficulty', '1HourShares',
            '1HourEstimatedShares', '1HourAmount', '24HourTotal', '24HourValid', '24HourOrphan', '24HourDifficulty',
            '24HourShares', '24HourEstimatedShares', '24HourAmount', '7DaysTotal', '7DaysValid', '7DaysOrphan',
            '7DaysDifficulty', '7DaysShares', '7DaysEstimatedShares', '7DaysAmount', '4WeeksTotal', '4WeeksValid',
            '4WeeksOrphan', '4WeeksDifficulty', '4WeeksShares', '4WeeksEstimatedShares', '4WeeksAmount', '12MonthTotal',
            '12MonthValid', '12MonthOrphan', '12MonthDifficulty', '12MonthShares', '12MonthEstimatedShares',
            '12MonthAmount']

@fixture
def get_blocks_found_keys():
    return ['id', 'height', 'blockhash', 'confirmations', 'amount', 'difficulty',
            'time', 'accounted', 'account_id', 'worker_name', 'shares', 'share_id',
            'finder', 'is_anonymous', 'estshares']


@fixture
def get_dashboard_keys():
    return ['raw', 'personal', 'balance', 'balance_for_auto_exchange', 'balance_on_exchange', 'recent_credits',
            'pool', 'system', 'network']


@fixture
def get_hourly_hash_rate_keys():
    return ['id', 'username', 'hashrate']


@fixture
def public_keys():
    return ['pool_name', 'hashrate', 'workers', 'shares_this_round', 'last_block', 'network_hashrate']


@fixture
def get_auto_switching_and_profits_statistics_keys():
    return ['algo', 'current_mining_coin', 'current_mining_coin_symbol', 'host', 'all_host_list', 'port',
            'algo_switch_port', 'multialgo_switch_port', 'profit', 'normalized_profit_amd', 'normalized_profit_nvidia']


@fixture
def get_mining_profit_and_statistics_keys():
    return ['coin_name', 'symbol', 'host', 'host_list', 'port', 'direct_mining_host', 'direct_mining_host_list',
            'direct_mining_algo_port', 'algo', 'normalized_profit', 'normalized_profit_amd', 'normalized_profit_nvidia',
            'profit', 'pool_hash', 'net_hash', 'difficulty', 'reward', 'last_block', 'time_since_last_block',
            'time_since_last_block_in_words', 'dovewallet_buy_price', 'bittrex_buy_price', 'poloniex_buy_price',
            'highest_buy_price', 'fee', 'workers']


@fixture
def get_user_all_balances_keys():
    return ['coin', 'confirmed', 'unconfirmed', 'ae_confirmed', 'ae_unconfirmed', 'exchange']


@vcr.use_cassette('vcr_cassettes/coin_name-get_block_count.yml', filter_query_parameters=['api_key'])
def test_get_block_count():
    """Tests an API call to get block count data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_block_count()

    assert isinstance(response, int)


@vcr.use_cassette('vcr_cassettes/coin_name-get_block_stats.yml', filter_query_parameters=['api_key'])
def test_get_block_stats(get_block_stats_keys):
    """Tests an API call to get block stats data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_block_stats()

    assert isinstance(response, dict)
    assert set(get_block_stats_keys).issubset(response.keys()), "All keys should be in the response"


@vcr.use_cassette('vcr_cassettes/coin_name-get_blocks_found.yml', filter_query_parameters=['api_key'])
def test_get_blocks_found(get_blocks_found_keys):
    """Tests an API call to get blocks found data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_blocks_found()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(get_blocks_found_keys).issubset(response[0].keys()), "All keys should be in the response"


@vcr.use_cassette('vcr_cassettes/coin_name-get_current_workers.yml', filter_query_parameters=['api_key'])
def test_get_current_workers():
    """Tests an API call to get current worker hash rate data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_current_workers()

    assert isinstance(response, int)


@vcr.use_cassette('vcr_cassettes/coin_name-get_dashboard.yml', filter_query_parameters=['api_key'])
def test_get_dashboard(get_dashboard_keys):
    """Tests an API call to get dashboard data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_dashboard()

    assert isinstance(response, dict)
    assert response['pool']['info']['currency'] == 'ETH', \
        'The coin name should be in the response'
    assert set(get_dashboard_keys).issubset(response.keys()), "All keys should be in the response"


@vcr.use_cassette('vcr_cassettes/coin_name-get_difficulty.yml', filter_query_parameters=['api_key'])
def test_get_difficulty():
    """Tests an API call to get difficulty data for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_difficulty()

    assert isinstance(response, int)


@vcr.use_cassette('vcr_cassettes/coin_name-get_estimated_time.yml', filter_query_parameters=['api_key'])
def test_get_difficulty():
    """Tests an API call to get estimated time for a coin_name"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_estimated_time()

    assert isinstance(response, int)


@vcr.use_cassette('vcr_cassettes/coin_name-get_hourly_hash_rate.yml', filter_query_parameters=['api_key'])
def test_get_hourly_hash_rate(get_hourly_hash_rate_keys):
    """Tests an API call to get hourly hash rate data for a pool"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_hourly_hash_rate()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(get_hourly_hash_rate_keys).issubset(response[0].keys())


@vcr.use_cassette('vcr_cassettes/coin_name-get_nav_bar_data.yml', filter_query_parameters=['api_key'])
def test_get_nav_bar_data():
    """Tests an API call to get nav bar data for a pool"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_nav_bar_data()

    assert isinstance(response, dict)
    assert response['error'] == 'disabled', \
        'The endpoint is disabled'


@vcr.use_cassette('vcr_cassettes/coin_name-public.yml', filter_query_parameters=['api_key'])
def test_public(public_keys):
    """Tests an API call to get public data for a a pool"""
    pool_instance = Pool('ethereum')
    response = pool_instance.public()

    assert isinstance(response, dict)
    assert set(public_keys).issubset(response.keys())


@vcr.use_cassette('vcr_cassettes/coin_name-get_auto_switching_and_profits_statistics.yml',
                  filter_query_parameters=['api_key'])
def test_get_auto_switching_and_profits_statistics(get_auto_switching_and_profits_statistics_keys):
    """Tests an API call to get mining profit and statistics"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_auto_switching_and_profits_statistics()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(get_auto_switching_and_profits_statistics_keys).issubset(response[0].keys())


@vcr.use_cassette('vcr_cassettes/coin_name-get_mining_profit_and_statistics.yml', filter_query_parameters=['api_key'])
def test_get_mining_profit_and_statistics(get_mining_profit_and_statistics_keys):
    """Tests an API call to get mining profit and statistics"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_mining_profit_and_statistics()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(get_mining_profit_and_statistics_keys).issubset(response[0].keys())


@vcr.use_cassette('vcr_cassettes/coin_name-get_user_all_balances_keys.yml',
                  filter_query_parameters=['api_key'])
def test_get_user_all_balances(get_user_all_balances_keys):
    """Tests an API call to get mining profit and statistics"""
    pool_instance = Pool('ethereum')
    response = pool_instance.get_user_all_balances()

    assert isinstance(response, list)
    assert isinstance(response[0], dict)
    assert set(get_user_all_balances_keys).issubset(response[0].keys())
