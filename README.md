# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-25
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
* [The Results](#the-results-2021-11-25)
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

## The Results (2021-11-25)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4968%2C4764%2C4684%2C4266%2C4033%2C3651%2C3559%2C3427%2C2730%2C2113%2C1909%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4968 | 6.17 | 6.97 | 6.45
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4764 | 6.32 | 7.58 | 6.77
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4684 | 6.34 | 7.84 | 6.90
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4266 | 6.93 | 8.59 | 7.52
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 4033 | 7.54 | 8.71 | 7.93
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3651 | 8.20 | 9.97 | 8.82
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3559 | 7.61 | 10.19 | 9.41
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3427 | 8.03 | 11.15 | 9.57
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2730 | 11.33 | 13.05 | 11.77
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2113 | 13.24 | 15.72 | 15.23
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1909 | 16.52 | 17.21 | 16.75


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3660%2C3316%2C2759%2C1953%2C1796%2C1738%2C1733%2C1697%2C1381%2C1146%2C165%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3660 | 7.96 | 10.26 | 8.74
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3316 | 8.81 | 10.43 | 9.68
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2759 | 9.74 | 13.31 | 11.78
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1953 | 14.65 | 18.67 | 16.38
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1796 | 16.20 | 18.79 | 17.81
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1738 | 16.05 | 19.61 | 18.62
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1733 | 15.63 | 20.34 | 20.13
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1697 | 17.32 | 18.54 | 18.84
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1381 | 22.92 | 23.57 | 23.16
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1146 | 27.50 | 29.66 | 27.89
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 165 | 183.78 | 193.66 | 192.51


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4367%2C4056%2C3893%2C3321%2C3304%2C3187%2C2477%2C2349%2C2105%2C1752%2C1391%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4367 | 7.07 | 8.14 | 7.32
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4056 | 7.80 | 8.53 | 7.87
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3893 | 7.88 | 9.19 | 8.25
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3321 | 9.46 | 10.53 | 9.61
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3304 | 8.59 | 10.72 | 10.23
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3187 | 9.48 | 11.24 | 10.10
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2477 | 10.94 | 13.10 | 13.14
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2349 | 11.87 | 17.03 | 14.26
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2105 | 14.66 | 15.26 | 15.21
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1752 | 18.04 | 18.64 | 18.23
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1391 | 22.46 | 25.09 | 22.96


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4531%2C4435%2C4199%2C3661%2C3443%2C3363%2C3300%2C2986%2C2337%2C2302%2C1936%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4531 | 6.77 | 8.02 | 7.05
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4435 | 7.10 | 8.18 | 7.21
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4199 | 7.32 | 8.45 | 7.65
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3661 | 8.47 | 9.75 | 8.75
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3443 | 8.85 | 10.36 | 9.35
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3363 | 8.26 | 11.25 | 9.92
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3300 | 9.01 | 9.57 | 9.94
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2986 | 9.03 | 13.22 | 11.12
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2337 | 13.39 | 14.45 | 13.70
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2302 | 13.65 | 14.07 | 13.89
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1936 | 16.31 | 16.75 | 16.50


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3956%2C3266%2C2281%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3956 | 7.58 | 9.28 | 8.11
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3266 | 9.56 | 10.50 | 9.79
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2281 | 13.71 | 14.52 | 14.03


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B306%2C128%2C106%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 306 | 96.17 | 103.85 | 104.22
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 128 | 231.11 | 274.03 | 245.69
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 106 | 277.80 | 291.06 | 295.53


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2401%2C1180%2C1093%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2401 | 12.94 | 14.07 | 13.32
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1180 | 24.67 | 31.55 | 27.26
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1093 | 28.97 | 33.47 | 29.24


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4240%2C2632%2C2284%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 4240 | 7.33 | 8.05 | 7.58
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2632 | 10.42 | 15.09 | 12.33
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2284 | 13.67 | 14.79 | 14.01


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3847%2C2461%2C1977%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3847 | 7.96 | 9.02 | 8.34
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2461 | 11.75 | 15.60 | 13.16
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1977 | 15.84 | 17.01 | 16.18


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B282%2C136%2C70%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 282 | 104.88 | 110.55 | 113.41
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 136 | 212.51 | 264.38 | 232.65
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 70 | 438.84 | 448.06 | 453.16


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2103%2C1179%2C868%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2103 | 14.88 | 16.47 | 15.20
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1179 | 24.27 | 32.18 | 27.75
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 868 | 36.60 | 40.68 | 36.82


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3694%2C2721%2C2279%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3694 | 8.35 | 9.27 | 8.68
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2721 | 9.79 | 14.33 | 12.15
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2279 | 13.84 | 14.83 | 14.04


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)