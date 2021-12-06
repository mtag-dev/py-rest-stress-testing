from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, Response

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = Starlette()


# first add 30 more routes to load routing system
# ------------------------------------------------
for n in range(10):
    app.route(f"/route-get-{n}/{{part}}", methods=['GET'])(HTMLResponse('ok'))
    app.route(f"/route-post-{n}/{{part}}", methods=['POST'])(HTMLResponse('ok'))
    app.route(f"/route-put-{n}/{{part}}", methods=['PUT'])(HTMLResponse('ok'))


# raw scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/raw/{dynamic}', methods=['GET'])
async def raw_userinfo(request):
    async with pool as connection:
        return JSONResponse(await connection.get("userinfo.json"))


@app.route('/api/v1/sprint/raw/{dynamic}', methods=['GET'])
async def raw_sprint(request):
    async with pool as connection:
        return JSONResponse(await connection.get("sprint.json"))


# raw scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['POST'])
async def raw_create_task(request):
    await request.json()
    async with pool as connection:
        return JSONResponse(await connection.get("create-task.json"))


# raw scenario PUT
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['PUT'])
async def raw_update_task(request):
    await request.json()
    async with pool as connection:
        await connection.get("update-task.json")
        return Response(b'')
