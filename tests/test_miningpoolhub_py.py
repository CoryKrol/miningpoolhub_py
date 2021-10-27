import aiohttp

from miningpoolhub_py.exceptions import NotFoundError
from miningpoolhub_py import MiningPoolHubAPI
import pytest
from pytest import fixture

NOT_ALL_KEYS_PRESENT = "All keys should be in the response"


@fixture
def get_block_stats_keys():
    return [
        "Total",
        "TotalValid",
        "TotalOrphan",
        "TotalDifficulty",
        "TotalShares",
        "TotalEstimatedShares",
        "TotalAmount",
        "1HourTotal",
        "1HourValid",
        "1HourOrphan",
        "1HourDifficulty",
        "1HourShares",
        "1HourEstimatedShares",
        "1HourAmount",
        "24HourTotal",
        "24HourValid",
        "24HourOrphan",
        "24HourDifficulty",
        "24HourShares",
        "24HourEstimatedShares",
        "24HourAmount",
        "7DaysTotal",
        "7DaysValid",
        "7DaysOrphan",
        "7DaysDifficulty",
        "7DaysShares",
        "7DaysEstimatedShares",
        "7DaysAmount",
        "4WeeksTotal",
        "4WeeksValid",
        "4WeeksOrphan",
        "4WeeksDifficulty",
        "4WeeksShares",
        "4WeeksEstimatedShares",
        "4WeeksAmount",
        "12MonthTotal",
        "12MonthValid",
        "12MonthOrphan",
        "12MonthDifficulty",
        "12MonthShares",
        "12MonthEstimatedShares",
        "12MonthAmount",
    ]


@fixture
def get_blocks_found_keys():
    return [
        "id",
        "height",
        "blockhash",
        "confirmations",
        "amount",
        "difficulty",
        "time",
        "accounted",
        "account_id",
        "worker_name",
        "shares",
        "share_id",
        "finder",
        "is_anonymous",
        "estshares",
    ]


@fixture
def get_dashboard_keys():
    return [
        "raw",
        "personal",
        "balance",
        "balance_for_auto_exchange",
        "balance_on_exchange",
        "recent_credits",
        "pool",
        "system",
        "network",
    ]


@fixture
def get_hourly_hash_rate_keys():
    return ["id", "username", "hashrate"]


@fixture
def get_pool_info_keys():
    return [
        "currency",
        "coinname",
        "cointarget",
        "coindiffchangetarget",
        "stratumport",
        "payout_system",
        "confirmations",
        "min_ap_threshold",
        "max_ap_threshold",
        "reward_type",
        "reward",
        "txfee",
        "txfee_manual",
        "txfee_auto",
        "fees",
    ]


@fixture
def get_pool_status_keys():
    return [
        "pool_name",
        "hashrate",
        "efficiency",
        "workers",
        "currentnetworkblock",
        "nextnetworkblock",
        "lastblock",
        "networkdiff",
        "esttime",
        "estshares",
        "timesincelast",
        "nethashrate",
    ]


@fixture
def get_top_contributors_keys():
    return ["account", "hashrate"]


@fixture
def get_user_balance_keys():
    return ["confirmed", "unconfirmed"]


@fixture
def get_user_status_keys():
    return ["username", "shares", "hashrate", "sharerate"]


@fixture
def public_keys():
    return [
        "pool_name",
        "hashrate",
        "workers",
        "shares_this_round",
        "last_block",
        "network_hashrate",
    ]


@fixture
def get_user_transactions_keys():
    return [
        "id",
        "username",
        "type",
        "amount",
        "coin_address",
        "txid",
        "height",
        "blockhash",
        "confirmations",
    ]


@fixture
def get_user_workers_keys():
    return ["id", "username", "password", "monitor", "hashrate", "difficulty"]


@fixture
def get_auto_switching_and_profits_statistics_keys():
    return [
        "algo",
        "current_mining_coin",
        "current_mining_coin_symbol",
        "host",
        "all_host_list",
        "port",
        "algo_switch_port",
        "multialgo_switch_port",
        "profit",
        "normalized_profit_amd",
        "normalized_profit_nvidia",
    ]


@fixture
def get_mining_profit_and_statistics_keys():
    return [
        "coin_name",
        "symbol",
        "host",
        "host_list",
        "port",
        "direct_mining_host",
        "direct_mining_host_list",
        "direct_mining_algo_port",
        "algo",
        "normalized_profit",
        "normalized_profit_amd",
        "normalized_profit_nvidia",
        "profit",
        "pool_hash",
        "net_hash",
        "difficulty",
        "reward",
        "last_block",
        "time_since_last_block",
        "time_since_last_block_in_words",
        "dovewallet_buy_price",
        "bittrex_buy_price",
        "poloniex_buy_price",
        "highest_buy_price",
        "fee",
        "workers",
    ]


@fixture
def get_user_all_balances_keys():
    return [
        "coin",
        "confirmed",
        "unconfirmed",
        "ae_confirmed",
        "ae_unconfirmed",
        "exchange",
    ]


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_block_count():
    """Tests an API call to get block count data for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)

        response = await pool_instance.async_get_block_count()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_block_stats(get_block_stats_keys):
    """Tests an API call to get block stats data for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_block_stats()

        assert isinstance(response, dict)
        assert set(get_block_stats_keys).issubset(response.keys()), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_blocks_found(get_blocks_found_keys):
    """Tests an API call to get blocks found data for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_blocks_found()

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert set(get_blocks_found_keys).issubset(
            response[0].keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_current_workers():
    """Tests an API call to get current worker hash rate data for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_current_workers()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_dashboard(get_dashboard_keys):
    """Tests an API call to get dashboard data for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_dashboard()

        assert isinstance(response, dict)
        assert (
            response["pool"]["info"]["currency"] == "ETH"
        ), "The coin name should be in the response"
        assert set(get_dashboard_keys).issubset(response.keys()), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_dashboard_invalid_name():
    """Tests an API call to get dashboard data for a coin_name that is invalid"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        with pytest.raises(NotFoundError):
            await pool_instance.async_get_dashboard(coin_name="poocash")


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_difficulty():
    """Tests an API call to get difficulty data for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_difficulty()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_difficulty():
    """Tests an API call to get estimated time for a coin_name"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_estimated_time()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_hourly_hash_rate(get_hourly_hash_rate_keys):
    """Tests an API call to get hourly hash rate data for a pool"""
    async with aiohttp.ClientSession() as session:
        api_instance = MiningPoolHubAPI(session=session)
        response = await api_instance.async_get_hourly_hash_rate()

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert set(get_hourly_hash_rate_keys).issubset(
            response[0].keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_nav_bar_data():
    """Tests an API call to get nav bar data for a pool"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_nav_bar_data()

        assert isinstance(response, dict)
        assert response["error"] == "disabled", "The endpoint is disabled"


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_pool_hash_rate():
    """Tests an API call to get pool hash rate"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_pool_hash_rate()

        assert isinstance(response, float)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_pool_info(get_pool_info_keys):
    """Tests an API call to get pool info"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_pool_info()

        assert isinstance(response, dict)
        assert set(get_pool_info_keys).issubset(response.keys()), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_pool_share_rate():
    """Tests an API call to get pool share rate"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_pool_share_rate()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_pool_status(get_pool_status_keys):
    """Tests an API call to get pool status"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_pool_status()

        assert isinstance(response, dict)
        assert set(get_pool_status_keys).issubset(response.keys()), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_time_since_last_block():
    """Tests an API call to get time since last block found"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_time_since_last_block()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_top_contributors(get_top_contributors_keys):
    """Tests an API call to get top contributor information"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_top_contributors()

        assert isinstance(response, dict)
        assert set(get_top_contributors_keys).issubset(
            response.keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_user_balance(get_user_balance_keys):
    """Tests an API call to get user balance information"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_user_balance()

        assert isinstance(response, dict)
        assert set(get_user_balance_keys).issubset(
            response.keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_user_hash_rate():
    """Tests an API call to get user hash rate"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_user_hash_rate()

        assert isinstance(response, float)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_user_share_rate():
    """Tests an API call to get user share rate"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_user_share_rate()

        assert isinstance(response, int)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_user_status(get_user_status_keys):
    """Tests an API call to get user status"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_user_status()

        assert isinstance(response, dict)
        assert set(get_user_status_keys).issubset(response.keys()), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_user_transactions(get_user_transactions_keys):
    """Tests an API call to get user transactions"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_user_transactions()

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert set(get_user_transactions_keys).issubset(
            response[0].keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_public(public_keys):
    """Tests an API call to get public data for a a pool"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_public()

        assert isinstance(response, dict)
        assert set(public_keys).issubset(response.keys()), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_auto_switching_and_profits_statistics(
    get_auto_switching_and_profits_statistics_keys,
):
    """Tests an API call to get mining profit and statistics"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_auto_switching_and_profits_statistics()

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert set(get_auto_switching_and_profits_statistics_keys).issubset(
            response[0].keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_mining_profit_and_statistics(get_mining_profit_and_statistics_keys):
    """Tests an API call to get mining profit and statistics"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_mining_profit_and_statistics()

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert set(get_mining_profit_and_statistics_keys).issubset(
            response[0].keys()
        ), NOT_ALL_KEYS_PRESENT


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_user_all_balances(get_user_all_balances_keys):
    """Tests an API call to get mining profit and statistics"""
    async with aiohttp.ClientSession() as session:
        pool_instance = MiningPoolHubAPI(session=session)
        response = await pool_instance.async_get_user_all_balances()

        assert isinstance(response, list)
        assert isinstance(response[0], dict)
        assert set(get_user_all_balances_keys).issubset(
            response[0].keys()
        ), NOT_ALL_KEYS_PRESENT
