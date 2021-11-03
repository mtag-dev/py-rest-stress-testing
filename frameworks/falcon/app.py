from falcon.asgi import App
from json import dumps

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


class userinfo:
    async def on_get(self, request, response, dynamic):
        async with pool as connection:
            response.text = dumps(await connection.get("userinfo.json"))


class sprint:
    async def on_get(self, request, response, dynamic):
        async with pool as connection:
            response.text = dumps(await connection.get("sprint.json"))


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
app.add_route('/api/v1/userinfo/{dynamic:int}', userinfo())
app.add_route('/api/v1/sprint/{dynamic:int}', sprint())
