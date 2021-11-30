# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-30
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
* [The Results](#the-results-2021-11-30)
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

## The Results (2021-11-30)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4871%2C4649%2C4636%2C4459%2C4348%2C3970%2C3433%2C3374%2C2576%2C1798%2C1708%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4871 | 11.99 | 13.18 | 13.26
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4649 | 12.68 | 13.93 | 13.94
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4636 | 12.62 | 13.80 | 14.42
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4459 | 13.50 | 14.79 | 14.39
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4348 | 13.66 | 14.65 | 14.86
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3970 | 15.00 | 16.31 | 16.18
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3433 | 16.76 | 21.73 | 18.96
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3374 | 16.39 | 21.51 | 19.10
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2576 | 22.36 | 27.86 | 25.35
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1798 | 33.70 | 38.73 | 35.61
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1708 | 35.88 | 37.28 | 37.57


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3345%2C3254%2C2893%2C1991%2C1809%2C1809%2C1705%2C1696%2C1149%2C1140%2C197%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3345 | 17.36 | 20.57 | 19.19
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3254 | 18.07 | 20.63 | 19.72
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2893 | 19.66 | 23.94 | 22.47
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1991 | 30.54 | 32.33 | 32.21
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1809 | 33.38 | 35.80 | 35.43
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1809 | 33.87 | 35.68 | 35.37
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1705 | 33.08 | 37.69 | 69.04
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1696 | 35.49 | 38.95 | 37.76
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1149 | 53.14 | 54.79 | 56.45
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1140 | 52.80 | 56.84 | 56.22
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 197 | 317.66 | 322.68 | 322.48


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4326%2C4323%2C4086%2C3900%2C3543%2C3186%2C3173%2C2957%2C1709%2C1605%2C1568%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4326 | 13.54 | 15.73 | 14.88
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4323 | 13.69 | 14.85 | 14.84
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4086 | 14.59 | 15.58 | 15.69
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3900 | 15.02 | 16.93 | 16.59
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3543 | 15.78 | 19.12 | 18.33
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3186 | 18.05 | 22.70 | 20.15
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3173 | 19.49 | 21.24 | 20.21
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2957 | 19.91 | 23.71 | 21.72
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1709 | 35.69 | 39.94 | 37.47
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1605 | 39.24 | 40.71 | 39.85
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1568 | 37.63 | 42.09 | 40.79


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4591%2C4497%2C4459%2C4322%2C3709%2C3583%2C3456%2C3132%2C2381%2C1994%2C1858%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4591 | 12.94 | 13.93 | 14.00
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4497 | 13.26 | 14.54 | 14.24
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4459 | 13.26 | 15.29 | 14.40
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4322 | 13.77 | 15.09 | 14.92
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3709 | 15.10 | 18.07 | 17.54
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3583 | 17.40 | 18.76 | 17.94
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3456 | 16.59 | 20.64 | 18.60
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3132 | 18.25 | 22.49 | 20.58
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2381 | 23.69 | 28.95 | 26.98
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1994 | 31.61 | 32.98 | 32.32
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1858 | 32.56 | 37.22 | 34.49


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4181%2C3231%2C2220%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 4181 | 14.05 | 15.55 | 15.44
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3231 | 18.20 | 21.67 | 19.85
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2220 | 25.93 | 31.72 | 29.29


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B633%2C173%2C131%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 633 | 98.06 | 100.72 | 100.98
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 173 | 361.26 | 369.52 | 368.53
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 131 | 470.80 | 487.00 | 480.97


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2386%2C1593%2C1188%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2386 | 24.25 | 29.85 | 26.87
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1593 | 36.92 | 42.90 | 40.17
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1188 | 49.06 | 56.12 | 54.21


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4145%2C3299%2C2278%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 4145 | 14.23 | 15.64 | 15.54
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3299 | 17.48 | 21.39 | 19.47
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2278 | 25.01 | 30.09 | 28.62


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B11692%2C3184%2C2020%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 11692 | 5.24 | 5.38 | 5.46
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3184 | 18.26 | 21.95 | 20.17
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2020 | 28.79 | 33.70 | 32.17


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B12152%2C188%2C88%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 12152 | 4.98 | 5.12 | 5.26
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 188 | 328.63 | 337.83 | 335.49
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 88 | 702.44 | 716.28 | 713.64


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B12497%2C1622%2C972%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 12497 | 4.66 | 4.98 | 5.11
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1622 | 36.45 | 42.36 | 39.47
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 972 | 62.82 | 68.09 | 65.96


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B12486%2C3336%2C2316%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 12486 | 4.67 | 5.34 | 5.29
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3336 | 17.27 | 21.23 | 19.38
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2316 | 25.05 | 28.66 | 27.76


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)