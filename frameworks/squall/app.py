from squall import Squall, Body
from squall.responses import HTMLResponse, PlainTextResponse

from schema_dataclasses import UserInfoResponse as DataClassesUserInfoResponse
from schema_dataclasses import SprintResponse as DataClassesSprintResponse
from schema_dataclasses import CreateTaskRequestBody as DataClassesCreateTaskRequestBody
from schema_dataclasses import CreateTaskResponse as DataClassesCreateTaskResponse
from schema_dataclasses import UpdateTaskRequestBody as DataClassesUpdateTaskRequestBody

# from schema_pydantic import UserInfoResponse as PydanticUserInfoResponse
# from schema_pydantic import SprintResponse as PydanticSprintResponse
# from schema_pydantic import CreateTaskRequestBody as PydanticCreateTaskRequestBody
# from schema_pydantic import CreateTaskResponse as PydanticCreateTaskResponse
# from schema_pydantic import UpdateTaskRequestBody as PydanticUpdateTaskRequestBody


from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = Squall()


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(part: int):
    return HTMLResponse('ok')

for n in range(10):
    app.get(f"/route-get-{n}/{{part}}")(req_any)
    app.post(f"/route-post-{n}/{{part}}")(req_any)
    app.put(f"/route-put-{n}/{{part}}")(req_any)


# raw scenario GET
# ------------------------------------------------
@app.get("/api/v1/userinfo/raw/{dynamic}")
async def raw_userinfo(dynamic: int):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.get("/api/v1/sprint/raw/{dynamic}")
async def raw_sprint(dynamic: int):
    async with pool as connection:
        return await connection.get("sprint.json")


# dataclasses scenario GET
# ------------------------------------------------
@app.get("/api/v1/userinfo/dataclasses/{dynamic}", response_model=DataClassesUserInfoResponse)
async def dataclasses_userinfo(dynamic: int):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.get("/api/v1/sprint/dataclasses/{dynamic}", response_model=DataClassesSprintResponse)
async def dataclasses_sprint(dynamic: int):
    async with pool as connection:
        return await connection.get("sprint.json")


# pydantic scenario GET
# ------------------------------------------------
# @app.get("/api/v1/userinfo/pydantic/{dynamic}", response_model=PydanticUserInfoResponse)
# async def pydantic_userinfo(dynamic: int):
#     async with pool as connection:
#         return await connection.get("userinfo.json")
#
#
# @app.get("/api/v1/sprint/pydantic/{dynamic}", response_model=PydanticSprintResponse)
# async def pydantic_sprint(dynamic: int):
#     async with pool as connection:
#         return await connection.get("sprint.json")


# raw scenario POST
# ------------------------------------------------
@app.post("/api/v1/board/raw/{dynamic}/task")
async def raw_create_task(dynamic: int, body=Body(...)):
    print(body)
    async with pool as connection:
        return await connection.get("create-task.json")


# dataclasses scenario POST
# ------------------------------------------------
@app.post("/api/v1/board/dataclasses/{dynamic}/task", response_model=DataClassesCreateTaskResponse)
async def dataclasses_create_task(dynamic: int, data: DataClassesCreateTaskRequestBody):
    async with pool as connection:
        return await connection.get("create-task.json")


# # pydantic scenario POST
# # ------------------------------------------------
# @app.post("/api/v1/board/pydantic/{dynamic}/task", response_model=PydanticCreateTaskResponse)
# async def pydantic_create_task(dynamic: int, data: PydanticCreateTaskRequestBody):
#     async with pool as connection:
#         return await connection.get("create-task.json")


# raw scenario PUT
# ------------------------------------------------
@app.put("/api/v1/board/raw/{dynamic}/task")
async def raw_update_task(dynamic: int, body=Body(...)):
    async with pool as connection:
        await connection.get("update-task.json")
        return ''


# dataclasses scenario PUT
# ------------------------------------------------
@app.put("/api/v1/board/dataclasses/{dynamic}/task")
async def dataclasses_update_task(dynamic: int, data: DataClassesUpdateTaskRequestBody):
    async with pool as connection:
        await connection.get("update-task.json")
        return ''


# # pydantic scenario PUT
# # ------------------------------------------------
# @app.put("/api/v1/board/pydantic/{dynamic}/task")
# async def pydantic_update_task(dynamic: int, data: PydanticUpdateTaskRequestBody):
#     async with pool as connection:
#         await connection.get("update-task.json")
#         return ''
