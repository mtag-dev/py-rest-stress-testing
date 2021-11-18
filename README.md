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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22squall-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5012%2C4709%2C4631%2C4343%2C4150%2C4017%2C3705%2C3632%2C2686%2C2140%2C1955%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 5012 | 6.12 | 6.69 | 6.59
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4709 | 6.39 | 7.50 | 6.84
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4631 | 6.54 | 7.74 | 6.92
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4343 | 6.72 | 7.92 | 7.47
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4150 | 7.04 | 8.82 | 8.01
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 4017 | 7.56 | 8.81 | 7.96
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3705 | 8.19 | 9.78 | 8.69
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3632 | 8.21 | 9.84 | 8.94
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2686 | 11.18 | 13.42 | 12.03
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2140 | 12.80 | 13.48 | 17.20
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1955 | 16.09 | 16.62 | 16.35


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3685%2C3069%2C2290%2C1968%2C1938%2C1762%2C1563%2C1558%2C1323%2C1176%2C159%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3685 | 7.92 | 10.08 | 8.69
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3069 | 9.39 | 10.76 | 10.51
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2290 | 12.21 | 15.98 | 14.24
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1968 | 14.62 | 18.16 | 16.26
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1938 | 14.96 | 18.00 | 16.49
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1762 | 16.44 | 19.36 | 18.15
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1563 | 17.47 | 23.48 | 21.71
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1558 | 18.47 | 22.78 | 20.56
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1323 | 23.14 | 23.93 | 24.33
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1176 | 26.74 | 28.72 | 27.16
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 159 | 189.99 | 199.19 | 200.35


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4688%2C4092%2C4026%2C3532%2C3433%2C3171%2C3149%2C3061%2C1788%2C1636%2C1167%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4688 | 6.59 | 7.49 | 6.82
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4092 | 7.42 | 8.38 | 7.88
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4026 | 7.52 | 9.15 | 7.94
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3532 | 8.67 | 10.56 | 9.05
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3433 | 9.00 | 10.23 | 9.36
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3171 | 8.99 | 10.91 | 10.39
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3149 | 8.74 | 11.48 | 11.13
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3061 | 9.19 | 11.28 | 10.99
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1788 | 17.50 | 18.21 | 17.87
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1636 | 14.77 | 23.11 | 20.46
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1167 | 25.12 | 32.15 | 27.66


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5080%2C4991%2C4973%2C4681%2C4406%2C3804%2C3456%2C3412%2C3333%2C2086%2C1463%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 5080 | 6.15 | 6.75 | 6.40
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4991 | 5.72 | 6.99 | 6.45
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4973 | 6.56 | 7.04 | 6.47
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4681 | 5.85 | 7.60 | 6.87
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4406 | 6.54 | 8.65 | 7.40
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3804 | 8.64 | 9.64 | 8.45
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3456 | 8.17 | 11.28 | 9.49
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3412 | 8.03 | 11.83 | 10.21
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 3333 | 9.83 | 10.79 | 9.70
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 2086 | 15.36 | 15.99 | 15.32
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1463 | 18.65 | 29.67 | 22.91


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3116%2C2892%2C2180%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3116 | 9.93 | 11.46 | 10.31
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2892 | 9.86 | 12.21 | 11.27
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2180 | 13.65 | 14.94 | 14.75


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B246%2C132%2C105%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 246 | 120.55 | 147.11 | 129.77
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 132 | 222.23 | 268.04 | 239.88
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 105 | 277.47 | 306.79 | 300.17


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1648%2C1477%2C460%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1648 | 17.59 | 21.39 | 19.68
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1477 | 20.95 | 24.46 | 21.65
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 460 | 62.87 | 88.53 | 71.66


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22squall-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3716%2C2440%2C2401%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3716 | 8.83 | 9.41 | 8.66
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2440 | 11.49 | 15.10 | 13.12
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2401 | 11.77 | 16.04 | 14.34


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3084%2C1851%2C1792%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3084 | 9.95 | 11.74 | 10.41
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1851 | 13.17 | 23.78 | 19.30
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1792 | 15.62 | 19.04 | 18.25


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B261%2C122%2C56%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 261 | 110.73 | 123.74 | 122.54
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 122 | 224.65 | 305.52 | 259.35
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 56 | 539.83 | 642.79 | 553.58


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1686%2C1450%2C745%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1686 | 18.15 | 21.45 | 19.03
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1450 | 20.57 | 23.73 | 22.21
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 745 | 38.12 | 48.48 | 43.28


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3761%2C2682%2C2447%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3761 | 8.65 | 9.19 | 8.58
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2682 | 11.38 | 13.05 | 12.22
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2447 | 12.21 | 14.98 | 13.09


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)