from muffin import Application, Response

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())

app = Application(debug=True)


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(request):
    return 'ok'


for n in range(10):
    app.route(f"/route-get-{n}/{{part}}", methods=['GET'])(req_any)
    app.route(f"/route-post-{n}/{{part}}", methods=['POST'])(req_any)
    app.route(f"/route-put-{n}/{{part}}", methods=['PUT'])(req_any)


# raw scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/raw/{dynamic}', methods=['GET'])
async def raw_userinfo(request):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.route('/api/v1/sprint/raw/{dynamic}', methods=['GET'])
async def raw_sprint(request):
    async with pool as connection:
        return await connection.get("sprint.json")


# raw scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['POST'])
async def raw_create_task(request):
    async with pool as connection:
        return await connection.get("create-task.json")


# raw scenario PUT
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['PUT'])
async def raw_update_task(request):
    async with pool as connection:
        return Response(b'')
