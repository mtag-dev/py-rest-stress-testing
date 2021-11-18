from aiohttp.web import RouteTableDef, Application, Response, json_response, HTTPNoContent

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


# raw scenario GET
# ------------------------------------------------
@routes.get("/api/v1/userinfo/raw/{dynamic}")
async def raw_userinfo(request):
    async with pool as connection:
        return json_response(await connection.get("userinfo.json"))


@routes.get("/api/v1/sprint/raw/{dynamic}")
async def raw_sprint(request):
    async with pool as connection:
        return json_response(await connection.get("sprint.json"))


# raw scenario POST
# ------------------------------------------------
@routes.post("/api/v1/board/raw/{dynamic}/task")
async def raw_create_task(request):
    async with pool as connection:
        return json_response(await connection.get("create-task.json"))


# raw scenario PUT
# ------------------------------------------------
@routes.put("/api/v1/board/raw/{dynamic}/task")
async def raw_update_task(request):
    async with pool as connection:
        return Response(text='')


app = Application()
app.add_routes(routes)
