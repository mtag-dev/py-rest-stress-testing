from aiohttp.web import (
    RouteTableDef, Application, Response, json_response, HTTPBadRequest, HTTPUnauthorized)

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())

routes = RouteTableDef()


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(request):
    return Response(text='ok')

for n in range(10):
    routes.get(f"/route-get-{n}/{{part}}")(req_any)
    routes.post(f"/route-post-{n}/{{part}}")(req_any)
    routes.put(f"/route-put-{n}/{{part}}")(req_any)


# then prepare endpoints for the benchmark
# ----------------------------------------
@routes.get("/api/v1/userinfo/{dynamic}")
async def handler(request):
    async with pool as connection:
        return json_response(await connection.get("userinfo.json"))


@routes.get("/api/v1/sprint/{dynamic}")
async def handler(request):
    async with pool as connection:
        return json_response(await connection.get("sprint.json"))


app = Application()
app.add_routes(routes)
