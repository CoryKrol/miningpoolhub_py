# import asyncio
# import aiohttp
# from yarl import URL
# from aiohttp import ClientSession
# from asynctest import CoroutineMock, patch
#
# from miningpoolhub_py.client import MiningPoolHubClient
# import pytest
# from pytest import fixture
#
#
# @patch('aiohttp.ClientSession.request')
# async def test_client_request(mock_request):
#     mock_request.return_value.__aenter__.json = CoroutineMock(side_effect= {'value': 'success'})
#     session = aiohttp.ClientSession()
#     client = MiningPoolHubClient(session=session, api_key='test')
#     resp = await client.get_request(URL('https://example.com'))
#
#     assert resp.status == 200
#
