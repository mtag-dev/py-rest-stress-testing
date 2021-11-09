from baize.asgi import (
    Router,
    Response,
    HTMLResponse,
    JSONResponse,
    Request,
    request_response,
)

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())

routes = []

# first add ten more routes to load routing system
# ------------------------------------------------
for n in range(10):
    routes.append((f"/route-get-{n}/{{part}}", HTMLResponse("ok")))
    routes.append((f"/route-post-{n}/{{part}}", HTMLResponse("ok")))
    routes.append((f"/route-put-{n}/{{part}}", HTMLResponse("ok")))


# raw scenario GET
# ------------------------------------------------
@request_response
async def raw_userinfo(request: Request) -> Response:
    async with pool as connection:
        return JSONResponse(await connection.get("userinfo.json"))


@request_response
async def raw_sprint(request: Request) -> Response:
    async with pool as connection:
        return JSONResponse(await connection.get("sprint.json"))


# raw scenario POST
# ------------------------------------------------
@request_response
async def raw_create_task(request: Request) -> Response:
    async with pool as connection:
        return JSONResponse(await connection.get("create-task.json"))

app = Router(
    *routes,
    ("/api/v1/userinfo/raw/{dynamic}", raw_userinfo),
    ("/api/v1/sprint/raw/{dynamic}", raw_sprint),
    ("/api/v1/board/raw/{dynamic}/task", raw_create_task),
)
