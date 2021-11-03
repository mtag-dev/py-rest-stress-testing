import pathlib
import random
from importlib import import_module

import pytest
from aiohttp.test_utils import TestClient, TestServer


@pytest.fixture(scope='module')
def app():
    return import_module('.aiohttp.app', package='frameworks').app


@pytest.fixture(scope='module')
async def aiohttp_client(app):
    server = TestServer(app)
    client = TestClient(server)
    await client.start_server()
    yield client
    await client.close()


async def test_api(aiohttp_client, fixtures):
    rand = random.randint(10, 99)
    url = f"/api/v1/userinfo/{rand}"
    res = await aiohttp_client.get(url)
    assert res.status == 200
    assert 'application/json' in res.headers.get('content-type', "")
    json = await res.json()
    assert json == fixtures['userinfo.json']['response']['payload']


async def test_routing(aiohttp_client):
    rand = random.randint(10, 99)
    for n in range(10):
        res = await aiohttp_client.get(f"/route-get-{n}/{rand}")
        assert res.status == 200
        res = await aiohttp_client.post(f"/route-post-{n}/{rand}", json={'foo': 'bar'})
        assert res.status == 200
        res = await aiohttp_client.put(f"/route-put-{n}/{rand}", json={'foo': 'bar'})
        assert res.status == 200

