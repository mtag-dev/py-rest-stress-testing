from sanic import Sanic
from sanic.response import html, json

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


# raw scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/raw/<dynamic:int>', methods=['GET'])
async def raw_userinfo(request, dynamic):
    async with pool as connection:
        return json(await connection.get("userinfo.json"))


@app.route('/api/v1/sprint/raw/<dynamic:int>', methods=['GET'])
async def raw_sprint(request, dynamic):
    async with pool as connection:
        return json(await connection.get("sprint.json"))


# raw scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/raw/<dynamic:int>/task', methods=['POST'])
async def raw_create_task(request, dynamic):
    async with pool as connection:
        return json(await connection.get("create-task.json"))
