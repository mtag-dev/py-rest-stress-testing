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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4770%2C4564%2C4360%2C4005%2C3758%2C3650%2C3620%2C3448%2C1951%2C1631%2C1173%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4770 | 6.43 | 7.41 | 6.75
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4564 | 6.41 | 7.75 | 7.29
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4360 | 6.97 | 8.29 | 7.35
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 4005 | 7.62 | 8.66 | 7.98
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3758 | 8.13 | 9.45 | 8.59
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3650 | 7.60 | 9.74 | 9.03
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3620 | 8.45 | 10.01 | 8.90
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3448 | 8.14 | 10.53 | 9.51
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1951 | 12.92 | 17.74 | 18.07
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1631 | 14.87 | 27.75 | 21.45
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1173 | 20.36 | 33.60 | 28.86


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22falcon-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2899%2C2795%2C2717%2C1963%2C1850%2C1795%2C1696%2C1642%2C1035%2C820%2C136%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2899 | 9.07 | 12.42 | 11.55
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2795 | 10.38 | 12.30 | 11.48
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2717 | 10.46 | 13.20 | 12.07
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1963 | 14.58 | 18.34 | 16.30
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1850 | 15.68 | 18.69 | 17.28
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1795 | 16.08 | 19.42 | 17.82
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1696 | 17.39 | 19.40 | 18.85
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1642 | 17.21 | 21.57 | 19.95
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1035 | 24.68 | 35.94 | 31.54
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 820 | 31.27 | 46.73 | 41.05
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 136 | 203.97 | 246.15 | 236.99


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22baize-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4187%2C3819%2C3717%2C3678%2C3570%2C3472%2C3367%2C3177%2C1503%2C1316%2C1129%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4187 | 7.29 | 8.52 | 7.66
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3819 | 7.94 | 9.62 | 8.36
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3717 | 7.98 | 9.65 | 8.63
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3678 | 7.82 | 9.81 | 8.91
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3570 | 8.71 | 9.62 | 9.00
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3472 | 8.84 | 10.25 | 9.20
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3367 | 9.10 | 10.88 | 9.54
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3177 | 8.74 | 11.37 | 10.49
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1503 | 20.10 | 22.15 | 21.32
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1316 | 21.57 | 27.36 | 24.82
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1129 | 24.08 | 36.06 | 29.54


</details>

<h3 id="update-task-raw"> Update task (PATCH) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22emmett-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22blacksheep-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B8841%2C8195%2C7865%2C6378%2C5918%2C4272%2C3930%2C3395%2C2465%2C2361%2C1817%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 8841 | 3.04 | 4.45 | 3.89
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 8195 | 3.40 | 4.57 | 4.08
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 7865 | 3.49 | 4.60 | 4.05
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 6378 | 4.53 | 5.58 | 5.07
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 5918 | 4.58 | 5.78 | 5.42
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 4272 | 6.35 | 8.81 | 7.70
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3930 | 7.76 | 9.42 | 8.13
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3395 | 9.27 | 9.66 | 9.40
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2465 | 11.39 | 13.57 | 13.77
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 2361 | 10.62 | 17.37 | 14.46
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1817 | 13.68 | 21.28 | 20.78


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3322%2C3246%2C1740%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3322 | 9.38 | 10.29 | 9.63
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3246 | 9.56 | 10.98 | 9.90
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1740 | 16.12 | 21.08 | 18.94


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B300%2C141%2C91%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 300 | 99.11 | 104.83 | 106.31
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 141 | 205.51 | 226.55 | 225.41
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 91 | 317.69 | 362.89 | 346.75


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1766%2C1232%2C859%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1766 | 17.63 | 19.59 | 18.09
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1232 | 23.14 | 28.86 | 26.73
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 859 | 33.56 | 42.22 | 37.99


</details>

<h3 id="update-task-dataclass"> Update task (PATCH) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22blacksheep-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4721%2C2952%2C2001%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 4721 | 6.13 | 7.78 | 6.75
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2952 | 9.51 | 12.94 | 11.18
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2001 | 13.25 | 18.50 | 16.46


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3328%2C3088%2C1653%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3328 | 9.22 | 11.01 | 9.61
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3088 | 9.82 | 11.88 | 10.39
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1653 | 17.34 | 21.67 | 19.93


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B275%2C159%2C59%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 275 | 107.79 | 114.25 | 115.74
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 159 | 185.72 | 200.27 | 201.28
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 59 | 469.24 | 588.71 | 534.93


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1707%2C1161%2C744%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1707 | 18.32 | 19.84 | 18.72
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1161 | 24.07 | 31.35 | 28.90
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 744 | 40.54 | 48.72 | 43.26


</details>

<h3 id="update-task-pydantic"> Update task (PATCH) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22fastapi-pydantic%22%2C%22blacksheep-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4614%2C3009%2C1714%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 4614 | 6.00 | 7.96 | 6.92
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 3009 | 8.63 | 12.47 | 11.34
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1714 | 12.81 | 24.21 | 20.43


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)