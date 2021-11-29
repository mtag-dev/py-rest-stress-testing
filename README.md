# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-29
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
* [The Results](#the-results-2021-11-29)
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

## The Results (2021-11-29)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4486%2C4449%2C4360%2C4296%2C4120%2C4040%2C3897%2C3586%2C2822%2C1961%2C1793%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4486 | 6.61 | 7.90 | 7.18
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4449 | 6.63 | 7.59 | 7.30
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4360 | 6.78 | 8.01 | 7.37
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4296 | 6.84 | 7.93 | 7.58
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4120 | 7.12 | 7.86 | 7.87
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4040 | 7.33 | 8.81 | 8.02
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3897 | 7.65 | 8.80 | 8.23
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3586 | 8.20 | 10.11 | 9.01
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2822 | 10.25 | 13.32 | 11.43
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1961 | 15.59 | 17.25 | 16.32
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1793 | 17.73 | 18.25 | 17.88


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3522%2C3400%2C3136%2C1996%2C1934%2C1844%2C1801%2C1750%2C1229%2C1164%2C194%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3522 | 8.45 | 9.40 | 9.11
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3400 | 8.69 | 9.53 | 9.48
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3136 | 9.41 | 10.34 | 10.30
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1996 | 14.80 | 16.39 | 16.07
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1934 | 15.12 | 17.23 | 16.58
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1844 | 15.96 | 17.74 | 17.43
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1801 | 16.30 | 17.81 | 17.77
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1750 | 16.87 | 19.12 | 18.27
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1229 | 25.76 | 26.34 | 26.05
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1164 | 25.55 | 28.87 | 27.48
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 194 | 154.34 | 165.11 | 164.78


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4084%2C3861%2C3811%2C3661%2C3553%2C3315%2C3220%2C2961%2C1836%2C1602%2C1518%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4084 | 7.24 | 8.69 | 7.91
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3861 | 7.76 | 8.90 | 8.32
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3811 | 7.71 | 8.96 | 8.46
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3661 | 8.05 | 9.98 | 8.80
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3553 | 8.20 | 9.87 | 9.18
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3315 | 8.98 | 10.41 | 9.74
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3220 | 9.06 | 11.12 | 10.05
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2961 | 10.50 | 11.52 | 10.88
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1836 | 17.20 | 18.54 | 17.45
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1602 | 19.87 | 20.46 | 20.02
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1518 | 18.98 | 24.36 | 21.14


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4213%2C4206%2C4093%2C4071%2C3662%2C3603%2C3396%2C3328%2C2444%2C2028%2C1947%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4213 | 7.01 | 8.61 | 7.63
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4206 | 7.05 | 8.12 | 7.67
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4093 | 7.24 | 8.80 | 7.98
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4071 | 7.27 | 8.60 | 7.94
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3662 | 8.13 | 9.83 | 8.76
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3603 | 8.07 | 9.55 | 9.11
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3396 | 8.63 | 10.55 | 9.55
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3328 | 9.27 | 10.34 | 9.63
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2444 | 11.81 | 15.10 | 13.21
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 2028 | 15.44 | 16.73 | 15.81
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1947 | 16.20 | 16.78 | 16.46


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3964%2C3251%2C2433%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3964 | 7.52 | 8.90 | 8.13
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3251 | 9.06 | 10.69 | 9.88
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2433 | 12.19 | 14.63 | 13.26


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B629%2C171%2C130%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 629 | 47.50 | 50.00 | 50.87
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 171 | 173.18 | 185.21 | 186.61
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 130 | 230.12 | 248.65 | 243.66


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2550%2C1569%2C1194%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2550 | 11.32 | 14.42 | 12.60
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1569 | 18.35 | 22.65 | 20.44
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1194 | 24.71 | 30.34 | 26.83


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3909%2C3440%2C2219%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3909 | 7.52 | 9.15 | 8.25
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3440 | 8.63 | 10.42 | 9.39
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2219 | 12.83 | 15.87 | 14.48


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B11759%2C3297%2C2094%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 11759 | 2.36 | 2.57 | 2.71
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3297 | 8.86 | 11.07 | 9.77
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2094 | 13.85 | 17.27 | 15.36


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B11693%2C189%2C86%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 11693 | 2.48 | 2.56 | 2.73
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 189 | 158.16 | 169.55 | 168.89
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 86 | 343.20 | 358.93 | 368.64


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10331%2C1613%2C970%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10331 | 2.73 | 2.92 | 3.10
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1613 | 17.98 | 22.53 | 19.86
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 970 | 30.50 | 38.13 | 33.00


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10970%2C3472%2C2334%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10970 | 2.72 | 2.83 | 2.91
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3472 | 8.46 | 10.25 | 9.29
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2334 | 12.73 | 15.38 | 13.73


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)