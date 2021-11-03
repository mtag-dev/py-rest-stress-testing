from baize.asgi import (
    Router,
    Response,
    HTMLResponse,
    PlainTextResponse,
    JSONResponse,
    Request,
    request_response,
    HTTPException,
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


# then prepare endpoints for the benchmark
# ----------------------------------------
@request_response
async def userinfo(request: Request) -> Response:
    async with pool as connection:
        return JSONResponse(await connection.get("userinfo.json"))


@request_response
async def sprint(request: Request) -> Response:
    async with pool as connection:
        return JSONResponse(await connection.get("sprint.json"))


app = Router(
    *routes,
    ("/api/v1/userinfo/{dynamic}", userinfo),
    ("/api/v1/sprint/{dynamic}", sprint),
)
