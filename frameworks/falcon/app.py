import falcon
from falcon.asgi import App
from json import dumps

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())

# raw scenario GET
# ------------------------------------------------


class raw_userinfo:
    async def on_get(self, request, response, dynamic):
        async with pool as connection:
            response.text = dumps(await connection.get("userinfo.json"))


class raw_sprint:
    async def on_get(self, request, response, dynamic):
        async with pool as connection:
            response.text = dumps(await connection.get("sprint.json"))


class raw_task:
    # raw scenario POST
    # ------------------------------------------------
    async def on_post(self, request, response, dynamic):
        async with pool as connection:
            response.text = dumps(await connection.get("create-task.json"))

    # raw scenario PUT
    # ------------------------------------------------
    async def on_put(self, request, response, dynamic):
        async with pool as connection:
            response.text = b''


app = App()


# first add ten more routes to load routing system
# ------------------------------------------------
class req_any:

    async def on_get(self, *args, **kwargs):
        pass

    async def on_post(self, *args, **kwargs):
        pass

    async def on_put(self, *args, **kwargs):
        pass


for n in range(10):
    app.add_route(f"/route-get-{n}/{{part:int}}", req_any())
    app.add_route(f"/route-post-{n}/{{part:int}}", req_any())
    app.add_route(f"/route-put-{n}/{{part:int}}", req_any())

# then prepare endpoints for the benchmark
# ----------------------------------------
app.add_route('/api/v1/userinfo/raw/{dynamic:int}', raw_userinfo())
app.add_route('/api/v1/sprint/raw/{dynamic:int}', raw_sprint())
app.add_route('/api/v1/board/raw/{dynamic:int}/task', raw_task())
