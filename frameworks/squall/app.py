from dummy.pool import Connection, Pool
from schema_dataclasses import (CreateTaskRequestBody, CreateTaskResponse,
                                SprintResponse, UpdateTaskRequestBody,
                                UserInfoResponse)

from squall import Body, Squall
from squall.responses import HTMLResponse

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


# scenario GET without schema
# ------------------------------------------------
@app.get("/api/v1/userinfo/raw/{dynamic}")
async def raw_userinfo(dynamic: int):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.get("/api/v1/sprint/raw/{dynamic}")
async def raw_sprint(dynamic: int):
    async with pool as connection:
        return await connection.get("sprint.json")


# scenario GET with schema
# ------------------------------------------------
@app.get("/api/v1/userinfo/dataclasses/{dynamic}", response_model=UserInfoResponse)
async def dataclasses_userinfo(dynamic: int):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.get("/api/v1/sprint/dataclasses/{dynamic}", response_model=SprintResponse)
async def dataclasses_sprint(dynamic: int):
    async with pool as connection:
        return await connection.get("sprint.json")


# scenario POST without schema
# ------------------------------------------------
@app.post("/api/v1/board/raw/{dynamic}/task")
async def raw_create_task(dynamic: int, body=Body(...)):
    async with pool as connection:
        return await connection.get("create-task.json")


# scenario POST with schema
# ------------------------------------------------
@app.post("/api/v1/board/dataclasses/{dynamic}/task", response_model=CreateTaskResponse)
async def dataclasses_create_task(dynamic: int, data: CreateTaskRequestBody):
    async with pool as connection:
        return await connection.get("create-task.json")


# scenario PUT without schema
# ------------------------------------------------
@app.put("/api/v1/board/raw/{dynamic}/task")
async def raw_update_task(dynamic: int, body=Body(...)):
    async with pool as connection:
        await connection.get("update-task.json")
        return ''


# scenario PUT with schema
# ------------------------------------------------
@app.put("/api/v1/board/dataclasses/{dynamic}/task")
async def dataclasses_update_task(dynamic: int, data: UpdateTaskRequestBody):
    async with pool as connection:
        await connection.get("update-task.json")
        return ''
