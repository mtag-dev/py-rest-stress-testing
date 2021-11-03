from blacksheep import Application
from blacksheep.server.responses import html, json, bad_request, text, unauthorized

from schema_pydantic import UserInfoResponse, SprintResponse
from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = Application()


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(request):
    return html('ok')

for n in range(10):
    app.route(f"/route-get-{n}/{{part}}", methods=['GET'])(req_any)
    app.route(f"/route-post-{n}/{{part}}", methods=['POST'])(req_any)
    app.route(f"/route-put-{n}/{{part}}", methods=['PUT'])(req_any)


# then prepare endpoints for the benchmark
# ----------------------------------------
@app.route('/api/v1/userinfo/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> UserInfoResponse:
    async with pool as connection:
        return UserInfoResponse(**(await connection.get("userinfo.json")))


@app.route('/api/v1/sprint/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> SprintResponse:
    async with pool as connection:
        return SprintResponse(**(await connection.get("sprint.json")))
