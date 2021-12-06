import os
import sys
import random
from importlib import import_module

import pytest

from dummy.pool import Pool, Connection

sys.path.append(os.path.join(os.getcwd(), "frameworks"))


@pytest.fixture(scope='function', params=[
    # 'aiohttp',  # doesnt support ASGI, implemented in separate test
    'quart',  # has to be first
    'baize',
    'blacksheep',
    'emmett',
    'falcon',
    'fastapi',
    'muffin',
    'sanic',
    'starlette',
])
def asgi(request):
    mod = import_module(f".{request.param}.app", package=__package__)
    mod.pool = Pool(data_getter=Connection())
    return mod.app


async def test_userinfo(client, fixtures):
    rand = random.randint(10, 99)
    url = f"/api/v1/userinfo/raw/{rand}"
    res = await client.get(url)
    assert res.status_code == 200
    assert 'application/json' in res.headers.get('content-type', "")
    json = await res.json()
    assert json == fixtures['userinfo.json']['response']['payload']


async def test_sprint(client, fixtures):
    rand = random.randint(10, 99)
    url = f"/api/v1/sprint/raw/{rand}"
    res = await client.get(url)
    assert res.status_code == 200
    assert 'application/json' in res.headers.get('content-type', "")
    json = await res.json()
    assert json == fixtures['sprint.json']['response']['payload']


async def test_create_task(client, fixtures):
    rand = random.randint(10, 99)
    url = f"/api/v1/board/raw/{rand}/task"
    res = await client.post(
        url, json=fixtures['create-task.json']['request']['payload'])
    assert res.status_code == 200
    assert 'application/json' in res.headers.get('content-type', "")
    json = await res.json()
    assert json == fixtures['create-task.json']['response']['payload']


async def test_update_task(client, fixtures):
    rand = random.randint(10, 99)
    url = f"/api/v1/board/raw/{rand}/task"
    res = await client.put(
        url, json=fixtures['update-task.json']['request']['payload'])
    assert res.status_code == 200
    data = res.content
    assert data == b''


async def test_routing(client):
    rand = random.randint(10, 99)
    for n in range(10):
        res = await client.get(f"/route-get-{n}/{rand}")
        assert res.status_code == 200
        res = await client.post(f"/route-post-{n}/{rand}", json={'foo': 'bar'})
        assert res.status_code == 200
        res = await client.put(f"/route-put-{n}/{rand}", json={'foo': 'bar'})
        assert res.status_code == 200


# Utils
# -----

def get_single(value):
    if isinstance(value, list):
        value, = value

    return value
