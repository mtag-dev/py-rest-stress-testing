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
    * TODO: [PATCH: Update issue](#update-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * TODO: [PATCH: Update issue](#update-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * [POST: Create issue](#create-pydantic)
    * TODO: [PATCH: Update issue](#update-pydantic)
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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5034%2C4364%2C4297%2C4257%2C3977%2C3729%2C3709%2C3682%2C2202%2C1560%2C1208%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 5034 | 6.06 | 6.65 | 6.36
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4364 | 6.46 | 8.05 | 8.03
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4297 | 6.70 | 8.43 | 7.67
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4257 | 6.89 | 8.19 | 7.63
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3977 | 7.35 | 8.95 | 8.20
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3729 | 7.79 | 9.42 | 8.75
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3709 | 7.86 | 9.86 | 8.83
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3682 | 8.24 | 9.66 | 8.79
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2202 | 12.62 | 16.31 | 14.93
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1560 | 17.01 | 21.72 | 21.21
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1208 | 25.88 | 28.08 | 26.55


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3381%2C3036%2C2187%2C1996%2C1914%2C1869%2C1295%2C1291%2C1156%2C826%2C157%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3381 | 8.09 | 10.72 | 9.77
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3036 | 9.19 | 11.86 | 10.77
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2187 | 11.58 | 16.69 | 15.05
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1996 | 14.27 | 18.11 | 16.04
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1914 | 14.81 | 18.26 | 16.76
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1869 | 15.48 | 18.54 | 17.10
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1295 | 19.41 | 29.76 | 26.73
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1291 | 19.76 | 29.40 | 26.32
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1156 | 27.26 | 29.26 | 27.84
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 826 | 26.48 | 52.09 | 41.09
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 157 | 187.15 | 205.24 | 202.73


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22emmett-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22squall-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4108%2C3900%2C3899%2C3811%2C3649%2C3457%2C3385%2C2105%2C1796%2C1733%2C1609%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4108 | 7.67 | 8.21 | 7.85
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3900 | 7.49 | 9.35 | 8.39
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3899 | 8.03 | 9.02 | 8.18
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3811 | 7.31 | 9.03 | 8.82
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3649 | 7.66 | 9.71 | 9.01
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3457 | 8.71 | 10.38 | 9.40
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3385 | 8.97 | 10.81 | 9.48
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2105 | 15.04 | 15.79 | 15.20
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1796 | 17.47 | 17.99 | 17.80
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1733 | 18.61 | 23.16 | 18.63
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1609 | 19.28 | 22.42 | 19.86


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22squall-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3206%2C2221%2C1884%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3206 | 9.31 | 11.07 | 10.13
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2221 | 13.88 | 15.09 | 14.49
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1884 | 12.74 | 23.61 | 19.21


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B202%2C128%2C102%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 202 | 151.50 | 157.72 | 157.87
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 128 | 230.06 | 272.89 | 251.52
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 102 | 289.15 | 316.68 | 310.59


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22squall-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1283%2C1069%2C864%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1283 | 22.28 | 28.22 | 25.27
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1069 | 29.62 | 33.45 | 29.90
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 864 | 33.69 | 42.84 | 37.72


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22fastapi-pydantic%22%2C%22blacksheep-pydantic%22%2C%22squall-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1966%2C1659%2C1645%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1966 | 15.47 | 16.39 | 16.31
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1659 | 18.68 | 24.60 | 19.61
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1645 | 19.97 | 24.27 | 19.54


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B185%2C126%2C65%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 185 | 163.56 | 171.88 | 171.17
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 126 | 215.94 | 306.56 | 255.32
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 65 | 453.37 | 497.65 | 487.29


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1513%2C1443%2C756%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1513 | 20.11 | 22.68 | 21.33
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1443 | 19.39 | 24.50 | 23.28
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 756 | 38.88 | 46.22 | 43.04


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)