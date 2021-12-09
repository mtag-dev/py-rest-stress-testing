# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-09
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
* [The Results](#the-results-2021-12-09)
* [JSON response without schema](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * [PUT: Update task](#update-task-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * [PUT: Update task](#update-task-dataclass)
    * [GET: Sprint board](#sprint-dataclass)


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

## The Results (2021-12-09)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3126%2C2962%2C2883%2C2798%2C2691%2C2531%2C2375%2C2288%2C1821%2C1366%2C1362%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 3126 | 19.32 | 22.76 | 20.55
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2962 | 20.48 | 24.01 | 21.63
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 2883 | 21.01 | 25.10 | 22.20
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 2798 | 21.94 | 26.44 | 22.92
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2691 | 22.88 | 27.17 | 23.75
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 2531 | 22.84 | 29.31 | 25.64
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 2375 | 26.02 | 30.95 | 26.92
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2288 | 25.69 | 32.54 | 28.05
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1821 | 34.31 | 39.94 | 35.11
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1366 | 45.07 | 49.01 | 46.82
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1362 | 46.09 | 50.98 | 46.95


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2209%2C1751%2C1554%2C1324%2C1274%2C1265%2C1132%2C990%2C844%2C794%2C168%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 2209 | 27.05 | 33.16 | 28.95
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 1751 | 34.47 | 42.03 | 36.47
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 1554 | 39.94 | 47.66 | 41.12
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 1324 | 45.36 | 55.31 | 48.28
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1274 | 46.97 | 58.63 | 50.13
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1265 | 47.53 | 59.25 | 50.50
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1132 | 52.56 | 66.18 | 56.42
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 990 | 61.37 | 74.61 | 64.61
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 844 | 74.04 | 82.23 | 75.57
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 794 | 78.12 | 84.74 | 80.46
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 168 | 362.79 | 451.56 | 374.16


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2803%2C2580%2C2555%2C2333%2C2272%2C2217%2C2107%2C1996%2C1351%2C1194%2C1091%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 2803 | 21.18 | 26.15 | 22.84
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2580 | 23.44 | 29.06 | 24.74
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 2555 | 23.67 | 29.14 | 24.99
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 2333 | 26.49 | 31.83 | 27.36
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2272 | 27.84 | 29.24 | 28.13
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 2217 | 27.48 | 33.30 | 28.87
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 2107 | 28.67 | 34.91 | 30.54
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 1996 | 30.09 | 36.30 | 32.15
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1351 | 46.70 | 51.54 | 47.32
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1194 | 51.27 | 55.97 | 53.54
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1091 | 58.88 | 67.46 | 58.51


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3074%2C2802%2C2713%2C2698%2C2609%2C2448%2C2277%2C2038%2C1536%2C1520%2C1451%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3074 | 19.75 | 23.73 | 20.76
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 2802 | 21.47 | 26.52 | 22.79
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 2713 | 21.43 | 27.31 | 23.62
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2698 | 23.43 | 24.71 | 23.69
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 2609 | 23.52 | 28.56 | 24.47
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 2448 | 24.26 | 30.30 | 26.16
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 2277 | 26.63 | 32.39 | 28.07
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2038 | 29.06 | 36.05 | 31.54
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1536 | 40.19 | 48.06 | 41.60
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1520 | 40.89 | 46.26 | 42.04
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1451 | 42.42 | 45.50 | 44.05


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2929%2C1953%2C1532%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2929 | 20.72 | 24.68 | 21.82
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1953 | 31.77 | 37.02 | 32.73
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1532 | 40.69 | 47.23 | 41.71


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B600%2C138%2C109%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 600 | 99.39 | 126.10 | 106.38
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 138 | 450.16 | 544.49 | 456.86
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 109 | 560.85 | 692.44 | 580.84


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1868%2C1023%2C819%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 1868 | 32.70 | 39.31 | 34.18
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1023 | 62.29 | 69.75 | 62.36
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 819 | 78.67 | 88.16 | 77.95


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2833%2C2013%2C1494%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2833 | 21.08 | 25.75 | 22.59
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 2013 | 30.82 | 36.29 | 31.73
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1494 | 41.43 | 49.14 | 42.73


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)