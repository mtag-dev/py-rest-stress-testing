# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-18
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
* [The Results](#the-results-2021-11-18)
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * [PUT: Update task](#update-task-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * [PUT: Update task](#update-task-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * [POST: Create task](#create-task-pydantic)
    * [PUT: Update task](#update-task-pydantic)
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

## The Results (2021-11-18)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22squall-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4713%2C4325%2C4043%2C3827%2C3619%2C3428%2C2952%2C2766%2C2515%2C2408%2C1898%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4713 | 6.39 | 7.43 | 7.16
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4325 | 6.83 | 8.21 | 7.51
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4043 | 7.13 | 8.92 | 8.15
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3827 | 7.83 | 9.26 | 8.39
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3619 | 7.41 | 10.38 | 9.25
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3428 | 8.71 | 10.55 | 9.44
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2952 | 8.43 | 11.73 | 13.34
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2766 | 10.90 | 12.76 | 11.63
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2515 | 12.57 | 12.84 | 12.72
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2408 | 12.17 | 15.13 | 13.61
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1898 | 16.30 | 17.13 | 16.87


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22emmett-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3142%2C2128%2C1873%2C1869%2C1790%2C1683%2C1666%2C1655%2C1347%2C1087%2C164%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3142 | 9.26 | 10.23 | 10.25
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2128 | 14.72 | 16.73 | 15.26
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1873 | 15.41 | 18.48 | 17.08
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1869 | 15.41 | 18.87 | 17.12
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 1790 | 11.49 | 30.05 | 20.49
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1683 | 16.42 | 21.15 | 19.35
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1666 | 16.75 | 21.17 | 19.27
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1655 | 17.75 | 19.55 | 19.32
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1347 | 22.95 | 23.63 | 24.06
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1087 | 27.67 | 31.09 | 29.62
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 164 | 179.62 | 192.46 | 193.82


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22squall-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4658%2C4170%2C4137%2C4074%2C3726%2C3586%2C3329%2C2300%2C2192%2C1669%2C1586%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4658 | 6.64 | 7.92 | 6.86
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4170 | 7.54 | 8.57 | 7.66
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4137 | 7.38 | 8.53 | 7.76
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4074 | 7.27 | 8.42 | 7.93
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3726 | 8.07 | 9.86 | 8.60
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3586 | 8.64 | 9.54 | 8.91
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3329 | 9.18 | 10.95 | 9.66
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2300 | 13.61 | 13.91 | 13.94
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2192 | 11.44 | 19.23 | 16.92
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1669 | 18.09 | 19.39 | 19.18
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1586 | 19.52 | 22.09 | 20.15


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22squall-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5158%2C4863%2C4661%2C4458%2C4051%2C3910%2C3434%2C2965%2C2944%2C2672%2C2023%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 5158 | 5.34 | 6.70 | 6.33
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4863 | 5.79 | 7.07 | 6.63
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4661 | 5.90 | 7.42 | 7.00
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4458 | 6.12 | 9.09 | 7.34
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 4051 | 6.81 | 9.14 | 7.96
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3910 | 6.86 | 10.22 | 9.61
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3434 | 8.96 | 10.57 | 9.49
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2965 | 10.22 | 12.05 | 11.45
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2944 | 9.01 | 13.60 | 13.24
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2672 | 11.70 | 12.24 | 12.00
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 2023 | 15.79 | 16.59 | 15.80


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3189%2C2618%2C2265%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3189 | 9.28 | 11.59 | 10.04
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2618 | 11.45 | 13.67 | 12.38
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2265 | 13.40 | 15.80 | 14.12


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B278%2C139%2C106%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 278 | 98.88 | 124.48 | 114.78
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 139 | 212.80 | 232.51 | 228.47
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 106 | 271.74 | 295.99 | 298.40


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1481%2C1278%2C1111%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1481 | 21.39 | 24.12 | 21.62
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1278 | 18.86 | 30.83 | 27.16
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1111 | 28.39 | 31.92 | 28.77


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3602%2C2283%2C2048%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3602 | 8.93 | 9.91 | 8.96
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2283 | 12.51 | 17.80 | 14.61
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2048 | 13.54 | 19.74 | 16.55


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3333%2C2474%2C2014%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3333 | 9.31 | 10.56 | 9.60
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2474 | 12.12 | 14.97 | 13.15
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2014 | 15.64 | 16.64 | 15.88


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B253%2C160%2C70%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 253 | 110.16 | 126.83 | 125.77
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 160 | 181.53 | 202.18 | 199.14
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 70 | 429.31 | 456.84 | 456.34


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1559%2C1285%2C872%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1559 | 20.09 | 22.35 | 20.51
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1285 | 20.93 | 29.63 | 27.58
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 872 | 36.21 | 40.59 | 36.69


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3735%2C2389%2C2247%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3735 | 8.69 | 9.79 | 8.64
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2389 | 11.82 | 16.44 | 27.80
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2247 | 12.36 | 17.10 | 14.62


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)