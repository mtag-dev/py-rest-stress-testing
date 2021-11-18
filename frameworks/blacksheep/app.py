from pydantic.dataclasses import dataclass as pydataclass

from blacksheep import Application
from blacksheep.server.responses import html, json, text
from blacksheep.server.bindings import FromJSON

from schema_dataclasses import UserInfoResponse as DataClassesUserInfoResponse
from schema_dataclasses import SprintResponse as DataClassesSprintResponse
from schema_dataclasses import CreateTaskRequestBody as DataClassesCreateTaskRequestBody
from schema_dataclasses import CreateTaskResponse as DataClassesCreateTaskResponse
from schema_dataclasses import UpdateTaskRequestBody as DataClassesUpdateTaskRequestBody

from schema_pydantic import UserInfoResponse as PydanticUserInfoResponse
from schema_pydantic import SprintResponse as PydanticSprintResponse
from schema_pydantic import CreateTaskRequestBody as PydanticCreateTaskRequestBody
from schema_pydantic import CreateTaskResponse as PydanticCreateTaskResponse
from schema_pydantic import UpdateTaskRequestBody as PydanticUpdateTaskRequestBody

from dummy.pool import Pool, Connection


pool = Pool(data_getter=Connection())


# FastAPI/Squall convert original dataclasses to pydantic dataclasses implicitly
# BlackSheep doesn't do it but there is an option just use pydantic dataclasses
# in order to make equal tests we set pydantic dataclasses here explicitly
# Check https://fastapi.tiangolo.com/advanced/dataclasses/
# Check https://www.neoteroi.dev/blacksheep/requests/#reading-json
DataClassesUserInfoResponse = pydataclass(DataClassesUserInfoResponse)
DataClassesSprintResponse = pydataclass(DataClassesSprintResponse)
DataClassesCreateTaskRequestBody = pydataclass(DataClassesCreateTaskRequestBody)
DataClassesCreateTaskResponse = pydataclass(DataClassesCreateTaskResponse)
DataClassesUpdateTaskRequestBody = pydataclass(DataClassesUpdateTaskRequestBody)


app = Application()


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(request):
    return html('ok')

for n in range(10):
    app.route(f"/route-get-{n}/{{part}}", methods=['GET'])(req_any)
    app.route(f"/route-post-{n}/{{part}}", methods=['POST'])(req_any)
    app.route(f"/route-put-{n}/{{part}}", methods=['PUT'])(req_any)


# raw scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/raw/{dynamic}', methods=['GET'])
async def get_userinfo(request):
    async with pool as connection:
        return json(await connection.get("userinfo.json"))


@app.route('/api/v1/sprint/raw/{dynamic}', methods=['GET'])
async def get_userinfo(request):
    async with pool as connection:
        return json(await connection.get("sprint.json"))


# dataclasses scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/dataclasses/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> DataClassesUserInfoResponse:
    async with pool as connection:
        return DataClassesUserInfoResponse(**(await connection.get("userinfo.json")))


@app.route('/api/v1/sprint/dataclasses/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> DataClassesSprintResponse:
    async with pool as connection:
        return DataClassesSprintResponse(**(await connection.get("sprint.json")))


# pydantic scenario GET
# ------------------------------------------------
@app.route('/api/v1/userinfo/pydantic/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> PydanticUserInfoResponse:
    async with pool as connection:
        return PydanticUserInfoResponse(**(await connection.get("userinfo.json")))


@app.route('/api/v1/sprint/pydantic/{dynamic}', methods=['GET'])
async def get_userinfo(request) -> PydanticSprintResponse:
    async with pool as connection:
        return PydanticSprintResponse(**(await connection.get("sprint.json")))


# raw scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['POST'])
async def raw_create_task(request):
    async with pool as connection:
        return json(await connection.get("create-task.json"))


# dataclasses scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/dataclasses/{dynamic}/task', methods=['POST'])
async def dataclasses_create_task(data: FromJSON[DataClassesCreateTaskRequestBody]) -> DataClassesCreateTaskResponse:
    async with pool as connection:
        return DataClassesCreateTaskResponse(**(await connection.get("create-task.json")))


# pydantic scenario POST
# ------------------------------------------------
@app.route('/api/v1/board/pydantic/{dynamic}/task', methods=['POST'])
async def pydantic_create_task(data: FromJSON[PydanticCreateTaskRequestBody]) -> PydanticCreateTaskResponse:
    async with pool as connection:
        return PydanticCreateTaskResponse(**(await connection.get("create-task.json")))


# raw scenario PUT
# ------------------------------------------------
@app.route('/api/v1/board/raw/{dynamic}/task', methods=['PUT'])
async def raw_update_task(request):
    async with pool as connection:
        return text('')


# dataclasses scenario PUT
# ------------------------------------------------
@app.route('/api/v1/board/dataclasses/{dynamic}/task', methods=['PUT'])
async def dataclasses_update_task(data: FromJSON[DataClassesUpdateTaskRequestBody]):
    async with pool as connection:
        return text('')


# pydantic scenario PUT
# ------------------------------------------------
@app.route('/api/v1/board/pydantic/{dynamic}/task', methods=['PUT'])
async def pydantic_update_task(data: FromJSON[PydanticUpdateTaskRequestBody]):
    async with pool as connection:
        return text('')
