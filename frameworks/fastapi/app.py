from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response

from dummy.pool import Pool, Connection
pool = Pool(data_getter=Connection())


app = FastAPI()


# first add 30 more routes to load routing system
# ------------------------------------------------
async def req_any(part: int):
    return HTMLResponse('ok')

for n in range(10):
    app.get(f"/route-get-{n}/{{part}}")(req_any)
    app.post(f"/route-post-{n}/{{part}}")(req_any)
    app.put(f"/route-put-{n}/{{part}}")(req_any)


@app.get("/api/v1/userinfo/{dynamic}")
async def userinfo(dynamic: int):
    async with pool as connection:
        return await connection.get("userinfo.json")


@app.get("/api/v1/sprint/{dynamic}")
async def sprint(dynamic: int):
    async with pool as connection:
        return await connection.get("sprint.json")
