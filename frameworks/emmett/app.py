from emmett import App, response
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


# raw scenario GET
# ------------------------------------------------
@app.route("/api/v1/userinfo/raw/<int:dynamic>", methods=["get"])
@service.json
async def raw_userinfo(dynamic):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.route("/api/v1/sprint/raw/<int:dynamic>", methods=["get"])
@service.json
async def raw_sprint(dynamic):
    async with pool as connection:
        return await connection.get("sprint.json")


# raw scenario POST
# ------------------------------------------------
@app.route("/api/v1/board/raw/<int:dynamic>/task", methods=["post"])
@service.json
async def raw_create_task(dynamic):
    async with pool as connection:
        return await connection.get("create-task.json")


# raw scenario PUT
# ------------------------------------------------
@app.route("/api/v1/board/raw/<int:dynamic>/task", methods=["put"])
@service.json
async def raw_update_task(dynamic):
    async with pool as connection:
        return ""
