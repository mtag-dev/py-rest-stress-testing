import time
from uuid import uuid4

from quart import Quart, Response, request

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = Quart(__name__)


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(part):
    return Response('OK')

for n in range(10):
    app.route(f"/route-get-{n}/<int:part>", methods=['GET'])(req_any)
    app.route(f"/route-post-{n}/<int:part>", methods=['POST'])(req_any)
    app.route(f"/route-put-{n}/<int:part>", methods=['PUT'])(req_any)


# then prepare endpoints for the benchmark
# ----------------------------------------
@app.route('/api/v1/userinfo/<int:dynamic>', methods=['GET'])
async def userinfo(dynamic):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.route('/api/v1/sprint/<int:dynamic>', methods=['GET'])
async def sprint(dynamic):
    async with pool as connection:
        return await connection.get("sprint.json")
