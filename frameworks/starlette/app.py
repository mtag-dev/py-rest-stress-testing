from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = Starlette()


# first add 30 more routes to load routing system
# ------------------------------------------------
for n in range(10):
    app.route(f"/route-get-{n}/{{part}}", methods=['GET'])(HTMLResponse('ok'))
    app.route(f"/route-post-{n}/{{part}}", methods=['POST'])(HTMLResponse('ok'))
    app.route(f"/route-put-{n}/{{part}}", methods=['PUT'])(HTMLResponse('ok'))


@app.route('/api/v1/userinfo/{dynamic}', methods=['GET'])
async def api(request):
    async with pool as connection:
        return JSONResponse(await connection.get("userinfo.json"))


@app.route('/api/v1/sprint/{dynamic}', methods=['GET'])
async def api(request):
    async with pool as connection:
        return JSONResponse(await connection.get("sprint.json"))

