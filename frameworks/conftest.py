import os
import json
import glob
import time

import pytest

FIXTURES_DIR = 'fixtures'


@pytest.fixture(scope='session')
def aiolib():
    return ('asyncio', {'use_uvloop': False})


@pytest.fixture
def ts():
    return time.time()


@pytest.fixture
async def client(asgi):
    from asgi_tools.tests import ASGITestClient

    client = ASGITestClient(asgi)
    async with client.lifespan():
        yield client


@pytest.fixture(scope='session')
def fixtures():
    result = {}
    for fixture_file in glob.glob(os.path.join(FIXTURES_DIR, '*.json')):
        with open(fixture_file) as fh:
            filename = os.path.split(fixture_file)[-1]
            result[filename] = json.loads(fh.read())
    return result
