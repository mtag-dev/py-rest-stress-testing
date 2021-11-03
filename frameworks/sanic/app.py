from sanic import Sanic
from sanic.response import html, json, text

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())

app = Sanic("benchmark")


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(request, part):
    return html('ok')

for n in range(10):
    app.route(f"/route-get-{n}/<part:int>", methods=['GET'])(req_any)
    app.route(f"/route-post-{n}/<part:int>", methods=['POST'])(req_any)
    app.route(f"/route-put-{n}/<part:int>", methods=['PUT'])(req_any)


# then prepare endpoints for the benchmark
# ----------------------------------------
@app.route('/api/v1/userinfo/<dynamic:int>', methods=['GET'])
async def api(request, dynamic):
    async with pool as connection:
        return json(await connection.get("userinfo.json"))


@app.route('/api/v1/sprint/<dynamic:int>', methods=['GET'])
async def api(request, dynamic):
    async with pool as connection:
        return json(await connection.get("sprint.json"))
