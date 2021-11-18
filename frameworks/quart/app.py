
from quart import Quart, Response

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


# raw scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/raw/<int:dynamic>', methods=['GET'])
async def raw_userinfo(dynamic):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.route('/api/v1/sprint/raw/<int:dynamic>', methods=['GET'])
async def raw_sprint(dynamic):
    async with pool as connection:
        return await connection.get("sprint.json")


# raw scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/raw/<int:dynamic>/task', methods=['POST'])
async def raw_create_task(dynamic):
    async with pool as connection:
        return await connection.get("create-task.json")


# raw scenario PUT
# ------------------------------------------------
@app.route('/api/v1/board/raw/<int:dynamic>/task', methods=['PUT'])
async def raw_update_task(dynamic):
    async with pool as connection:
        return b''
