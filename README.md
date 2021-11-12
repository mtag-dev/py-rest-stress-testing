# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-12
#### Original benchmark: https://klen.github.io/py-frameworks-bench/

[![benchmarks](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/benchmarks.yml)
[![tests](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/tests.yml/badge.svg)](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/tests.yml)

----------

We aim to create a tool for technical decision-making.

This is a benchmark for modern ASGI micro-frameworks. 
Designed to be not one more "Hello world" benchmark, but cover some real-like 
scenarios instead. Doesn't provide composite scoring, drills down instead.

To be data source agnostic (API, DB, etc.) framework provides thread-safe async 
dummy pool with configurable size and data retrieving latency. Because of our 
target is benchmark web-frameworks itself, this feature by default configured 
with default pool size `10` and latency `1ms` (emulates very fast data source, 
like Redis.)

Through polls, we have found out that AVG mature service contains ~30 endpoints. 
So during a time, routing performance can drop. We cover this by adding 30 more 
dynamic endpoints with different methods. These endpoints are just present for 
routing cycle load.

This benchmark doesn't provide load tests for different ASGI servers. All tests 
(except AioHTTP) runs on the Uvicorn.

Doesn't contain benchmarks for OAuth 2.0/OIDC/JWT features. 
This is because we pretty sure that these features should be a part of API-Gateway 
and not in end service itself.

Further development implies adding scenarios from different domains. 
For now, it is only issue tracker as example

## Table of contents

* [The Methodic](#the-methodic)
* [The Results](#the-results-2021-11-12)
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * [PATCH: Update task](#update-task-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * [PATCH: Update task](#update-task-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * [POST: Create task](#create-task-pydantic)
    * [PATCH: Update task](#update-task-pydantic)
    * [GET: Sprint board](#sprint-pydantic)


## The Methodic

The benchmark runs as a [Github Action](https://github.com/features/actions).
According to the [github
documentation](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
the hardware specification for the runs is:

* 2-core vCPU (Intel® Xeon® Platinum 8272CL (Cascade Lake), Intel® Xeon® 8171M 2.1GHz (Skylake))
* 7 GB of RAM memory
* 14 GB of SSD disk space
* OS Ubuntu 20.04

[ASGI](https://asgi.readthedocs.io/en/latest/) apps are running from docker using the gunicorn/uvicorn command:

    gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 app:app

Applications' source code can be found
[here](https://github.com/mtag-dev/py-rest-stress-testing/tree/master/frameworks).

Results received with WRK utility using the params:

    wrk -d15s -t4 -c32 [URL]

The "Issue tracker" suite has a four kind of tests:
- getting user information
- create task
- update task
- board with short information with 100 issues on it

You can find test data [here](https://github.com/mtag-dev/py-rest-stress-testing/tree/master/fixtures).

## The Results (2021-11-12)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4797%2C4145%2C3388%2C3365%2C3300%2C2778%2C2767%2C2500%2C2379%2C1921%2C1286%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4797 | 6.28 | 7.40 | 6.71
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4145 | 6.99 | 8.69 | 7.92
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3388 | 7.93 | 10.33 | 10.71
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3365 | 8.86 | 10.94 | 9.54
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3300 | 9.25 | 11.05 | 9.72
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2778 | 10.83 | 13.13 | 11.79
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2767 | 11.02 | 13.31 | 11.58
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2500 | 12.61 | 12.89 | 12.80
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2379 | 12.71 | 15.78 | 13.55
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1921 | 15.76 | 19.39 | 16.85
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1286 | 24.46 | 26.29 | 24.87


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2504%2C2125%2C2038%2C1889%2C1396%2C1377%2C1257%2C1192%2C1137%2C814%2C169%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2504 | 12.02 | 14.27 | 12.80
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2125 | 14.12 | 16.55 | 15.24
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2038 | 14.69 | 16.98 | 15.80
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1889 | 15.31 | 18.36 | 16.94
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1396 | 21.37 | 24.61 | 22.92
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1377 | 21.50 | 25.68 | 23.23
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1257 | 23.23 | 27.30 | 25.51
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1192 | 24.33 | 29.12 | 26.86
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1137 | 23.39 | 29.57 | 28.74
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 814 | 37.66 | 42.27 | 39.28
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 169 | 170.02 | 189.87 | 187.55


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4212%2C3211%2C3046%2C2881%2C2876%2C2748%2C2571%2C2258%2C2246%2C1635%2C1299%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4212 | 7.25 | 8.68 | 7.61
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3211 | 9.46 | 11.43 | 10.03
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3046 | 10.01 | 12.12 | 10.51
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2881 | 10.48 | 12.47 | 11.27
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2876 | 10.73 | 12.85 | 11.11
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2748 | 11.24 | 13.48 | 11.64
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2571 | 11.67 | 14.26 | 12.56
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2258 | 13.45 | 16.45 | 14.26
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2246 | 13.63 | 13.97 | 14.60
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1635 | 19.04 | 21.49 | 19.55
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1299 | 24.30 | 25.79 | 24.61


</details>

<h3 id="update-task-raw"> Update task (PATCH) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22emmett-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B8305%2C7090%2C5612%2C4554%2C3780%2C3076%2C2867%2C2551%2C2544%2C2135%2C1700%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 8305 | 3.28 | 4.47 | 4.06
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 7090 | 3.82 | 5.60 | 4.64
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 5612 | 5.00 | 6.58 | 5.70
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 4554 | 5.98 | 8.44 | 7.08
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 3780 | 8.10 | 8.33 | 8.54
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3076 | 9.14 | 10.02 | 10.38
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2867 | 10.48 | 13.04 | 11.20
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2551 | 12.29 | 14.00 | 12.55
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2544 | 11.36 | 14.94 | 12.76
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2135 | 13.42 | 16.23 | 15.05
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1700 | 17.67 | 20.15 | 19.58


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3274%2C2359%2C2346%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3274 | 9.47 | 10.98 | 9.78
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2359 | 12.69 | 15.59 | 13.71
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2346 | 13.39 | 14.44 | 13.63


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B260%2C144%2C107%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 260 | 116.97 | 121.72 | 123.02
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 144 | 204.80 | 217.96 | 221.07
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 107 | 273.06 | 296.30 | 295.78


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1341%2C1266%2C995%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1341 | 21.53 | 26.33 | 24.36
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1266 | 24.42 | 29.16 | 25.27
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 995 | 30.30 | 35.77 | 32.55


</details>

<h3 id="update-task-dataclass"> Update task (PATCH) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2474%2C1919%2C1633%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2474 | 11.52 | 12.22 | 12.91
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1919 | 14.86 | 19.12 | 16.77
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1633 | 17.25 | 23.01 | 19.71


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3334%2C2336%2C2070%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3334 | 8.62 | 11.35 | 9.61
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2336 | 12.98 | 15.73 | 13.80
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2070 | 15.27 | 15.80 | 15.45


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B237%2C161%2C71%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 237 | 128.32 | 132.78 | 134.49
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 161 | 186.10 | 199.10 | 198.05
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 71 | 425.25 | 436.75 | 445.72


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1247%2C1181%2C637%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1247 | 23.40 | 30.73 | 25.98
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1181 | 26.09 | 31.53 | 27.10
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 637 | 48.83 | 56.65 | 50.12


</details>

<h3 id="update-task-pydantic"> Update task (PATCH) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2465%2C1951%2C1651%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2465 | 11.36 | 12.57 | 12.96
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1951 | 14.31 | 18.97 | 16.61
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1651 | 17.26 | 20.93 | 19.43


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)