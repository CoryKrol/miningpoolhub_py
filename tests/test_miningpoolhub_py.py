import aiohttp
import json

from miningpoolhub_py.exceptions import (
    APIError,
    APIRateLimitError,
    InvalidCoinError,
    UnauthorizedError,
)
from miningpoolhub_py import MiningPoolHubAPI
import pytest
from aioresponses import aioresponses

NOT_ALL_KEYS_PRESENT = "All keys should be in the response"

GET_USER_BALANCES_URL = "https://ethereum.miningpoolhub.com/index.php?action=getuserbalance&api_key=test&page=api"
GET_AUTO_SWITCHING_URL = "https://miningpoolhub.com/index.php?action=getautoswitchingandprofitsstatistics&page=api"

CONTENT_HEADERS = {"Content-Type": "text/html"}
ETHEREUM = "ethereum"


@pytest.mark.asyncio
async def test_unauthorized_api_key():
    """Tests an API call with a bad API key"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(GET_USER_BALANCES_URL, status=401)
        with pytest.raises(UnauthorizedError):
            await miningpoolhubapi.async_get_user_balance(coin_name=ETHEREUM)
    await session.close()


@pytest.mark.asyncio
async def test_bad_coin_name(get_auto_switching_and_profits_statistics_response):
    """Tests an API call with a non-existent coin name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://doggy_coin.miningpoolhub.com/index.php?action=getuserbalance&api_key=test&page=api",
            exception=aiohttp.ClientConnectionError(),
        )
        m.get(
            GET_AUTO_SWITCHING_URL,
            status=200,
            body=json.dumps(get_auto_switching_and_profits_statistics_response),
            headers=CONTENT_HEADERS,
        )
        with pytest.raises(InvalidCoinError):
            await miningpoolhubapi.async_get_user_balance(coin_name="doggy_coin")
    await session.close()


@pytest.mark.asyncio
async def test_bad_connection():
    """Tests an API call with a bad connection, to distinguish from a bad coin name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(GET_USER_BALANCES_URL, exception=aiohttp.ClientConnectionError())
        m.get(
            "https://miningpoolhub.com/index.php?action=getautoswitchingandprofitsstatistics&api_key=test&page=api",
            exception=aiohttp.ClientConnectionError(),
        )
        with pytest.raises(aiohttp.ClientConnectionError):
            await miningpoolhubapi.async_get_user_balance(coin_name=ETHEREUM)
    await session.close()


@pytest.mark.asyncio
async def test_api_rate_limit(api_rate_limit_response):
    """Tests an API call with a non-existent coin name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            GET_USER_BALANCES_URL,
            status=200,
            body=api_rate_limit_response,
            headers=CONTENT_HEADERS,
        )
        with pytest.raises(APIRateLimitError):
            await miningpoolhubapi.async_get_user_balance(coin_name=ETHEREUM)
    await session.close()


@pytest.mark.asyncio
async def test_get_block_count(get_block_count_response):
    """Tests an API call to get block count data for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getblockcount&api_key=test&page=api",
            status=200,
            body=json.dumps(get_block_count_response),
            headers=CONTENT_HEADERS,
        )

        resp = await miningpoolhubapi.async_get_block_count(coin_name=ETHEREUM)
        assert isinstance(resp, int)
        assert resp == 13503059

    await session.close()


@pytest.mark.asyncio
async def test_get_block_stats(get_block_stats_keys, get_block_stats_response):
    """Tests an API call to get block stats data for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getblockstats&api_key=test&page=api",
            status=200,
            payload=get_block_stats_response,
            headers=CONTENT_HEADERS,
        )

        result = await miningpoolhubapi.async_get_block_stats(coin_name=ETHEREUM)
        assert isinstance(result, dict)
        assert set(get_block_stats_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_blocks_found(get_blocks_found_keys, get_blocks_found_response):
    """Tests an API call to get blocks found data for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getblocksfound&api_key=test&page=api",
            status=200,
            body=json.dumps(get_blocks_found_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_blocks_found(coin_name=ETHEREUM)

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_blocks_found_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_current_workers(get_current_workers_response):
    """Tests an API call to get current worker hash rate data for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getcurrentworkers&api_key=test&page=api",
            status=200,
            body=json.dumps(get_current_workers_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_current_workers(coin_name=ETHEREUM)

        assert isinstance(result, int)
        assert result == 190057

    await session.close()


@pytest.mark.asyncio
async def test_get_dashboard(get_dashboard_keys, get_dashboard_data_response):
    """Tests an API call to get dashboard data for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getdashboarddata&api_key=test&page=api",
            status=200,
            body=json.dumps(get_dashboard_data_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_dashboard(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert (
            result["pool"]["info"]["currency"] == "ETH"
        ), "The coin name should be in the response"
        assert (
            result["balance_on_exchange"] is not None
        ), "Balance on exchange should not be null"
        assert result["balance_on_exchange"] == 0.1
        assert (
            result["personal"]["shares"]["valid"] is not None
        ), "Valid shares should not be null"
        assert result["personal"]["shares"]["valid"] == 12288
        assert (
            result["personal"]["shares"]["invalid"] is not None
        ), "Invalid shares should not be null"
        assert result["personal"]["shares"]["invalid"] == 1
        assert (
            result["pool"]["shares"]["valid"] is not None
        ), "Valid shares should not be null"
        assert result["pool"]["shares"]["valid"] == 2287112448
        assert (
            result["pool"]["shares"]["invalid"] is not None
        ), "Invalid shares should not be null"
        assert result["pool"]["shares"]["invalid"] == 2129568
        assert set(get_dashboard_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_dashboard_null_balance_on_exchange(
    get_dashboard_keys, get_dashboard_data_response
):
    """Tests an API call to get dashboard data for a coin_name"""
    get_dashboard_data_response["getdashboarddata"]["data"][
        "balance_on_exchange"
    ] = None
    get_dashboard_data_response["getdashboarddata"]["data"]["personal"]["shares"][
        "valid"
    ] = None
    get_dashboard_data_response["getdashboarddata"]["data"]["personal"]["shares"][
        "invalid"
    ] = None
    get_dashboard_data_response["getdashboarddata"]["data"]["pool"]["shares"][
        "valid"
    ] = None
    get_dashboard_data_response["getdashboarddata"]["data"]["pool"]["shares"][
        "invalid"
    ] = None
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getdashboarddata&api_key=test&page=api",
            status=200,
            body=json.dumps(get_dashboard_data_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_dashboard(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert (
            result["pool"]["info"]["currency"] == "ETH"
        ), "The coin name should be in the response"
        assert (
            result["balance_on_exchange"] is not None
        ), "Balance on exchange should not be null"
        assert result["balance_on_exchange"] == 0.0
        assert (
            result["personal"]["shares"]["valid"] is not None
        ), "Valid shares should not be null"
        assert result["personal"]["shares"]["valid"] == 0
        assert (
            result["personal"]["shares"]["invalid"] is not None
        ), "Invalid shares should not be null"
        assert result["personal"]["shares"]["invalid"] == 0
        assert (
            result["pool"]["shares"]["valid"] is not None
        ), "Valid shares should not be null"
        assert result["pool"]["shares"]["valid"] == 0
        assert (
            result["pool"]["shares"]["invalid"] is not None
        ), "Invalid shares should not be null"
        assert result["pool"]["shares"]["invalid"] == 0
        assert set(get_dashboard_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_difficulty(get_difficulty_response):
    """Tests an API call to get difficulty data for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getdifficulty&api_key=test&page=api",
            status=200,
            body=json.dumps(get_difficulty_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_difficulty(coin_name=ETHEREUM)

        assert isinstance(result, int)
        assert result == 10248372611623184

    await session.close()


@pytest.mark.asyncio
async def test_get_estimated_time(get_estimated_time_response):
    """Tests an API call to get estimated time for a coin_name"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getestimatedtime&api_key=test&page=api",
            status=200,
            body=json.dumps(get_estimated_time_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_estimated_time(coin_name=ETHEREUM)

        assert isinstance(result, int)
        assert result == 2059292915976

    await session.close()


@pytest.mark.asyncio
async def test_get_hourly_hash_rate(
    get_hourly_hash_rate_keys, get_hourly_hash_rates_response
):
    """Tests an API call to get hourly hash rate data for a pool"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=gethourlyhashrates&api_key=test&page=api",
            status=200,
            body=json.dumps(get_hourly_hash_rates_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_hourly_hash_rate(coin_name=ETHEREUM)

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_hourly_hash_rate_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_nav_bar_data(get_nav_bar_data_response):
    """Tests an API call to get nav bar data for a pool"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getnavbardata&api_key=test&page=api",
            status=200,
            body=json.dumps(get_nav_bar_data_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_nav_bar_data(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert result["error"] == "disabled", "The endpoint is disabled"

    await session.close()


@pytest.mark.asyncio
async def test_get_pool_hash_rate(get_pool_hash_rate_response):
    """Tests an API call to get pool hash rate"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getpoolhashrate&api_key=test&page=api",
            status=200,
            body=json.dumps(get_pool_hash_rate_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_pool_hash_rate(coin_name=ETHEREUM)

        assert isinstance(result, float)
        assert result == 21318913068.661

    await session.close()


@pytest.mark.asyncio
async def test_get_pool_info(get_pool_info_keys, get_pool_info_response):
    """Tests an API call to get pool info"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getpoolinfo&api_key=test&page=api",
            status=200,
            body=json.dumps(get_pool_info_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_pool_info(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(get_pool_info_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_pool_share_rate(get_pool_share_rate_response):
    """Tests an API call to get pool share rate"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getpoolsharerate&api_key=test&page=api",
            status=200,
            body=json.dumps(get_pool_share_rate_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_pool_share_rate(coin_name=ETHEREUM)

        assert isinstance(result, int)

    await session.close()


@pytest.mark.asyncio
async def test_get_pool_status(get_pool_status_keys, get_pool_status_response):
    """Tests an API call to get pool status"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getpoolstatus&api_key=test&page=api",
            status=200,
            body=json.dumps(get_pool_status_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_pool_status(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(get_pool_status_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_time_since_last_block(get_time_since_last_block_response):
    """Tests an API call to get time since last block found"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=gettimesincelastblock&api_key=test&page=api",
            status=200,
            body=json.dumps(get_time_since_last_block_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_time_since_last_block(
            coin_name=ETHEREUM
        )

        assert isinstance(result, int)
        assert result == 1153

    await session.close()


@pytest.mark.asyncio
async def test_get_top_contributors(
    get_top_contributors_keys, get_top_contributors_response
):
    """Tests an API call to get top contributor information"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=gettopcontributors&api_key=test&page=api",
            status=200,
            body=json.dumps(get_top_contributors_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_top_contributors(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(get_top_contributors_keys).issubset(
            result.keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_user_balance(get_user_balance_keys, get_user_balance_response):
    """Tests an API call to get user balance information"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            GET_USER_BALANCES_URL,
            status=200,
            body=json.dumps(get_user_balance_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_balance(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(get_user_balance_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_user_hash_rate(get_user_hash_rate_response):
    """Tests an API call to get user hash rate"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getuserhashrate&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_hash_rate_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_hash_rate(coin_name=ETHEREUM)

        assert isinstance(result, float)
        assert result == 200431.807

    await session.close()


@pytest.mark.asyncio
async def test_get_user_share_rate(get_user_share_rate_response):
    """Tests an API call to get user share rate"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getusersharerate&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_share_rate_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_share_rate(coin_name=ETHEREUM)

        assert isinstance(result, int)
        assert result == 0

    await session.close()


@pytest.mark.asyncio
async def test_get_user_status(get_user_status_keys, get_user_status_response):
    """Tests an API call to get user status"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getuserstatus&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_status_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_status(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(get_user_status_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT
        assert result["shares"] is not None, "Invalid shares should not be null"
        assert result["shares"] == 1

    await session.close()


@pytest.mark.asyncio
async def test_get_user_status_null_shares(
    get_user_status_keys, get_user_status_response
):
    """Tests an API call to get user status"""
    get_user_status_response["getuserstatus"]["data"]["shares"] = None
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getuserstatus&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_status_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_status(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(get_user_status_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT
        assert result["shares"] is not None, "Invalid shares should not be null"
        assert result["shares"] == 0

    await session.close()


@pytest.mark.asyncio
async def test_get_user_transactions(
    get_user_transactions_keys, get_user_transactions_response
):
    """Tests an API call to get user transactions"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getusertransactions&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_transactions_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_transactions(coin_name=ETHEREUM)

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_user_transactions_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_user_workers(get_user_workers_keys, get_user_workers_response):
    """Tests an API call to get user workers"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=getuserworkers&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_workers_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_workers(coin_name=ETHEREUM)

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_user_workers_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_public(public_keys, public_response):
    """Tests an API call to get public data for a a pool"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://ethereum.miningpoolhub.com/index.php?action=public&page=api",
            status=200,
            body=json.dumps(public_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_public(coin_name=ETHEREUM)

        assert isinstance(result, dict)
        assert set(public_keys).issubset(result.keys()), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_auto_switching_and_profits_statistics(
    get_auto_switching_and_profits_statistics_keys,
    get_auto_switching_and_profits_statistics_response,
):
    """Tests an API call to get auto switching profit and statistics"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            GET_AUTO_SWITCHING_URL,
            status=200,
            body=json.dumps(get_auto_switching_and_profits_statistics_response),
            headers=CONTENT_HEADERS,
        )
        result = (
            await miningpoolhubapi.async_get_auto_switching_and_profits_statistics()
        )

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_auto_switching_and_profits_statistics_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_auto_switching_and_profits_statistics_fail(
    get_auto_switching_and_profits_statistics_response_fail,
):
    """Tests an API call to get auto switching profit and statistics that failed"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            GET_AUTO_SWITCHING_URL,
            status=200,
            body=json.dumps(get_auto_switching_and_profits_statistics_response_fail),
            headers=CONTENT_HEADERS,
        )
        with pytest.raises(APIError):
            await miningpoolhubapi.async_get_auto_switching_and_profits_statistics()
    await session.close()


@pytest.mark.asyncio
async def test_get_mining_profit_and_statistics(
    get_mining_profit_and_statistics_keys,
    get_mining_and_profit_statistics_response,
):
    """Tests an API call to get auto switching profit and statistics that failed"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    with aioresponses() as m:
        m.get(
            "https://miningpoolhub.com/index.php?action=getminingandprofitsstatistics&page=api",
            status=200,
            body=json.dumps(get_mining_and_profit_statistics_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_mining_profit_and_statistics()

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_mining_profit_and_statistics_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()


@pytest.mark.asyncio
async def test_get_mining_profit_and_statistics_fail(
    get_mining_and_profit_statistics_response_fail,
):
    """Tests an API call to get mining profit and statistics"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    with aioresponses() as m:
        m.get(
            "https://miningpoolhub.com/index.php?action=getminingandprofitsstatistics&page=api",
            status=200,
            body=json.dumps(get_mining_and_profit_statistics_response_fail),
            headers=CONTENT_HEADERS,
        )
        with pytest.raises(APIError):
            await miningpoolhubapi.async_get_mining_profit_and_statistics()
    await session.close()


@pytest.mark.asyncio
async def test_get_user_all_balances(
    get_user_all_balances_keys, get_user_all_balances_response
):
    """Tests an API call to get mining profit and statistics"""
    session = aiohttp.ClientSession()
    miningpoolhubapi = MiningPoolHubAPI(session=session)
    assert miningpoolhubapi.api_key_set() is True
    with aioresponses() as m:
        m.get(
            "https://miningpoolhub.com/index.php?action=getuserallbalances&api_key=test&page=api",
            status=200,
            body=json.dumps(get_user_all_balances_response),
            headers=CONTENT_HEADERS,
        )
        result = await miningpoolhubapi.async_get_user_all_balances()

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(get_user_all_balances_keys).issubset(
            result[0].keys()
        ), NOT_ALL_KEYS_PRESENT

    await session.close()
