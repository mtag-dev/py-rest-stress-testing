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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4545%2C4078%2C4061%2C3846%2C3831%2C3781%2C3512%2C3463%2C2543%2C1733%2C1730%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4545 | 6.46 | 7.53 | 7.14
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4078 | 7.18 | 8.69 | 7.89
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4061 | 7.06 | 8.93 | 8.01
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3846 | 7.60 | 9.20 | 8.36
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3831 | 7.72 | 8.59 | 8.37
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3781 | 7.55 | 9.76 | 8.61
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3512 | 8.08 | 10.41 | 9.29
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3463 | 8.44 | 10.14 | 9.30
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2543 | 11.09 | 14.50 | 12.68
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1733 | 17.73 | 18.37 | 18.51
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1730 | 17.45 | 19.89 | 18.57


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3493%2C3238%2C2658%2C1805%2C1788%2C1696%2C1631%2C1579%2C1093%2C1083%2C177%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3493 | 8.46 | 9.51 | 9.23
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3238 | 8.95 | 11.11 | 9.95
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2658 | 10.62 | 13.48 | 12.33
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1805 | 15.49 | 20.23 | 17.85
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1788 | 16.04 | 19.65 | 18.11
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1696 | 17.60 | 19.25 | 18.89
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1631 | 17.49 | 21.84 | 19.68
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1579 | 17.84 | 23.54 | 20.41
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1093 | 26.98 | 31.62 | 29.33
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1083 | 27.07 | 31.00 | 29.55
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 177 | 167.11 | 186.92 | 179.76


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3773%2C3728%2C3352%2C3124%2C2986%2C2861%2C2607%2C2598%2C1782%2C1593%2C1429%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3773 | 7.81 | 9.10 | 8.53
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3728 | 7.81 | 9.82 | 8.61
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3352 | 8.55 | 10.91 | 9.72
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3124 | 9.28 | 11.72 | 10.42
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2986 | 9.61 | 12.07 | 11.03
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2861 | 9.96 | 12.77 | 11.41
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2607 | 11.42 | 13.43 | 12.36
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2598 | 10.32 | 13.83 | 13.49
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1782 | 17.40 | 19.11 | 17.97
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1593 | 19.82 | 20.39 | 20.09
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1429 | 20.17 | 25.38 | 22.43


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4072%2C3883%2C3660%2C3393%2C3074%2C3054%2C2930%2C2413%2C1903%2C1833%2C1828%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4072 | 7.15 | 8.92 | 7.88
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3883 | 7.56 | 9.30 | 8.35
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3660 | 7.87 | 10.18 | 8.89
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3393 | 8.75 | 10.89 | 9.58
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3074 | 9.40 | 11.70 | 10.64
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3054 | 9.88 | 11.36 | 10.53
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2930 | 9.76 | 12.52 | 11.16
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2413 | 11.94 | 15.12 | 13.79
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1903 | 16.38 | 17.05 | 16.87
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1833 | 16.22 | 18.40 | 17.61
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1828 | 16.33 | 20.27 | 17.73


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3754%2C2711%2C2319%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3754 | 7.83 | 9.65 | 8.60
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2711 | 10.43 | 13.52 | 11.96
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2319 | 12.02 | 16.08 | 13.92


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B629%2C152%2C132%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 629 | 47.39 | 51.37 | 50.97
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 152 | 191.66 | 236.72 | 210.45
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 132 | 228.36 | 287.16 | 242.42


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2382%2C1285%2C1092%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2382 | 11.89 | 15.23 | 13.56
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1285 | 23.20 | 28.27 | 24.98
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1092 | 26.22 | 34.07 | 29.38


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3395%2C3129%2C1951%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3395 | 8.35 | 10.92 | 9.55
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3129 | 9.23 | 11.74 | 10.36
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1951 | 14.64 | 19.02 | 16.64


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B12097%2C2871%2C2013%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 12097 | 2.34 | 2.59 | 2.63
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2871 | 10.04 | 12.73 | 11.33
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2013 | 13.86 | 18.22 | 15.94


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B11498%2C188%2C80%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 11498 | 2.51 | 2.62 | 2.77
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 188 | 156.22 | 167.99 | 169.16
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 80 | 363.16 | 401.52 | 392.01


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10546%2C1373%2C873%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10546 | 2.81 | 2.92 | 3.03
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1373 | 21.37 | 26.26 | 23.44
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 873 | 33.35 | 41.51 | 37.06


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B9365%2C2672%2C1934%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 9365 | 2.93 | 3.91 | 3.48
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2672 | 10.60 | 13.97 | 12.50
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1934 | 15.12 | 19.00 | 16.71


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)