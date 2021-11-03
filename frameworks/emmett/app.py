from emmett import App, request, response
from emmett.tools import service

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = App(__name__)
app.config.handle_static = False


# first add 30 more routes to load routing system
# ------------------------------------------------
@app.route(
    [f"/route-get-{n}/<int:part>" for n in range(10)],
    methods=["get"],
    output="str"
)
async def req_get(part=None):
    return 'ok'


@app.route(
    [f"/route-post-{n}/<int:part>" for n in range(10)],
    methods=["post"],
    output="str"
)
async def req_post(part=None):
    return 'ok'


@app.route(
    [f"/route-put-{n}/<int:part>" for n in range(10)],
    methods=["put"],
    output="str"
)
async def req_put(part=None):
    return 'ok'


# then prepare endpoints for the benchmark
# ----------------------------------------0
@app.route("/api/v1/userinfo/<int:dynamic>", methods=["get"])
@service.json
async def userinfo(dynamic):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.route("/api/v1/sprint/<int:dynamic>", methods=["get"])
@service.json
async def sprint(dynamic):
    async with pool as connection:
        return await connection.get("sprint.json")
