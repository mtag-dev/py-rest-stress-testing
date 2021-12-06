from dummy.pool import Connection, Pool
from pydantic.dataclasses import dataclass as pydataclass
from schema_dataclasses import (CreateTaskRequestBody, CreateTaskResponse,
                                SprintResponse, UpdateTaskRequestBody,
                                UserInfoResponse)

from blacksheep import Application
from blacksheep.server.bindings import FromJSON
from blacksheep.server.responses import html, json, text


pool = Pool(data_getter=Connection())


# FastAPI/Squall convert original dataclasses to pydantic dataclasses implicitly
# BlackSheep doesn't do it but there is an option just use pydantic dataclasses
# in order to make equal tests we set pydantic dataclasses here explicitly
# Check https://fastapi.tiangolo.com/advanced/dataclasses/
# Check https://www.neoteroi.dev/blacksheep/requests/#reading-json
UserInfoResponse = pydataclass(UserInfoResponse)
SprintResponse = pydataclass(SprintResponse)
CreateTaskRequestBody = pydataclass(CreateTaskRequestBody)
CreateTaskResponse = pydataclass(CreateTaskResponse)
UpdateTaskRequestBody = pydataclass(UpdateTaskRequestBody)


app = Application()


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(request):
    return html('ok')

for n in range(10):
    app.route(f"/route-get-{n}/{{part}}", methods=['GET'])(req_any)
    app.route(f"/route-post-{n}/{{part}}", methods=['POST'])(req_any)
    app.route(f"/route-put-{n}/{{part}}", methods=['PUT'])(req_any)


# scenario GET without schema
# ------------------------------------------------
@app.route('/api/v1/userinfo/raw/{dynamic}', methods=['GET'])
async def get_userinfo(request):
    async with pool as connection:
        return json(await connection.get("userinfo.json"))


@app.route('/api/v1/sprint/raw/{dynamic}', methods=['GET'])
async def get_userinfo(request):
    async with pool as connection:
        return json(await connection.get("sprint.json"))


# scenario GET with schema
# ------------------------------------------------
@app.route('/api/v1/userinfo/dataclasses/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> UserInfoResponse:
    async with pool as connection:
        return UserInfoResponse(**(await connection.get("userinfo.json")))


@app.route('/api/v1/sprint/dataclasses/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> SprintResponse:
    async with pool as connection:
        return SprintResponse(**(await connection.get("sprint.json")))


# scenario POST without schema
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['POST'])
async def raw_create_task(request):
    await request.json()
    async with pool as connection:
        return json(await connection.get("create-task.json"))


# scenario POST with schema
# ------------------------------------------------
@app.route('/api/v1/board/dataclasses/{dynamic}/task', methods=['POST'])
async def dataclasses_create_task(data: FromJSON[CreateTaskRequestBody]) -> CreateTaskResponse:
    async with pool as connection:
        return CreateTaskResponse(**(await connection.get("create-task.json")))


# scenario PUT without schema
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['PUT'])
async def raw_update_task(request):
    await request.json()
    async with pool as connection:
        await connection.get("update-task.json")
        return text('')


# scenario PUT with schema
# ------------------------------------------------
@app.route('/api/v1/board/dataclasses/{dynamic}/task', methods=['PUT'])
async def dataclasses_update_task(data: FromJSON[UpdateTaskRequestBody]):
    async with pool as connection:
        await connection.get("update-task.json")
        return text('')
