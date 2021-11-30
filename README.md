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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4894%2C4787%2C4695%2C4487%2C4340%2C4260%2C3871%2C3197%2C2544%2C1808%2C1724%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4894 | 11.78 | 13.31 | 13.22
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4787 | 12.42 | 13.66 | 13.42
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4695 | 12.78 | 13.73 | 13.70
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4487 | 12.74 | 15.31 | 14.39
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4340 | 13.57 | 15.10 | 14.86
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4260 | 13.74 | 14.86 | 15.27
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3871 | 15.06 | 16.86 | 16.61
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3197 | 17.44 | 22.38 | 20.10
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2544 | 22.56 | 28.05 | 25.27
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1808 | 33.25 | 37.87 | 35.38
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1724 | 36.36 | 37.39 | 37.14


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3482%2C3245%2C2878%2C1950%2C1812%2C1799%2C1770%2C1639%2C1136%2C1042%2C193%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3482 | 16.78 | 18.49 | 18.40
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3245 | 17.79 | 19.67 | 20.05
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2878 | 19.87 | 23.95 | 22.34
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1950 | 30.55 | 33.08 | 32.85
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1812 | 32.84 | 35.88 | 35.35
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1799 | 32.89 | 37.01 | 35.56
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1770 | 34.25 | 36.23 | 36.23
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1639 | 36.09 | 40.57 | 39.15
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1136 | 53.14 | 57.82 | 56.26
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1042 | 55.55 | 68.43 | 61.41
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 193 | 321.68 | 325.85 | 329.73


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4294%2C4165%2C3918%2C3819%2C3582%2C3163%2C3078%2C2847%2C1709%2C1530%2C1525%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4294 | 13.86 | 15.03 | 14.93
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4165 | 14.40 | 15.70 | 15.45
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3918 | 15.19 | 16.33 | 16.42
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3819 | 15.08 | 16.96 | 16.93
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3582 | 15.61 | 18.22 | 18.23
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3163 | 17.87 | 22.63 | 20.47
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3078 | 19.93 | 21.87 | 20.86
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2847 | 20.52 | 24.70 | 22.59
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1709 | 35.48 | 40.39 | 37.49
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1530 | 40.45 | 42.06 | 42.56
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1525 | 38.07 | 45.99 | 42.17


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4452%2C4452%2C4219%2C4187%2C3569%2C3533%2C3388%2C3106%2C2258%2C1989%2C1873%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4452 | 13.39 | 14.90 | 14.44
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4452 | 13.38 | 14.61 | 14.43
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4219 | 13.99 | 15.45 | 15.25
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4187 | 13.81 | 15.73 | 15.53
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3569 | 15.72 | 18.30 | 18.43
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3533 | 17.57 | 18.99 | 18.18
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3388 | 17.11 | 21.26 | 18.94
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3106 | 18.32 | 22.26 | 20.75
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2258 | 25.18 | 30.91 | 28.72
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1989 | 31.80 | 33.03 | 32.22
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1873 | 32.35 | 36.51 | 34.21


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4204%2C3051%2C2258%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 4204 | 14.00 | 15.40 | 15.33
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3051 | 18.90 | 23.16 | 21.04
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2258 | 25.46 | 31.63 | 28.39


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B632%2C170%2C130%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 632 | 98.18 | 101.44 | 101.04
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 170 | 371.33 | 374.08 | 373.51
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 130 | 482.12 | 495.81 | 489.65


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2322%2C1548%2C1170%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2322 | 24.58 | 31.18 | 27.67
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1548 | 38.74 | 42.42 | 41.32
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1170 | 50.22 | 58.02 | 54.79


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3561%2C3326%2C2190%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3561 | 15.74 | 20.15 | 18.11
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3326 | 17.32 | 21.41 | 19.29
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2190 | 26.36 | 32.25 | 29.23


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10885%2C3072%2C2017%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10885 | 5.24 | 5.49 | 6.19
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3072 | 18.82 | 22.85 | 20.84
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2017 | 28.91 | 34.21 | 31.74


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B11546%2C188%2C87%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 11546 | 5.22 | 5.37 | 5.56
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 188 | 323.12 | 334.72 | 336.99
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 87 | 698.31 | 739.67 | 730.12


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B12631%2C1598%2C955%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 12631 | 4.45 | 4.84 | 5.04
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1598 | 36.84 | 42.22 | 40.09
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 955 | 62.78 | 68.70 | 66.91


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10465%2C3244%2C2267%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10465 | 5.55 | 5.81 | 6.19
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3244 | 17.38 | 22.08 | 19.97
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2267 | 25.64 | 29.50 | 28.25


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)