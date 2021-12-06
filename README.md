# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-06
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
* [The Results](#the-results-2021-12-06)
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

## The Results (2021-12-06)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22blacksheep-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22baize-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3994%2C3920%2C3805%2C3636%2C3343%2C3080%2C2826%2C2438%2C1914%2C1857%2C1098%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3994 | 13.25 | 18.00 | 16.59
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3920 | 14.72 | 15.70 | 16.39
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3805 | 12.62 | 18.36 | 19.05
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3636 | 13.56 | 19.67 | 19.05
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3343 | 17.07 | 21.29 | 19.75
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3080 | 16.19 | 26.86 | 22.84
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2826 | 19.86 | 25.45 | 23.19
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2438 | 25.90 | 26.41 | 26.23
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1914 | 26.72 | 38.29 | 36.04
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1857 | 30.38 | 38.75 | 34.59
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1098 | 56.64 | 63.29 | 58.29


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22blacksheep-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2182%2C1991%2C1972%2C1662%2C1545%2C1506%2C1446%2C1228%2C1111%2C677%2C55%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2182 | 26.42 | 31.19 | 29.40
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 1991 | 29.98 | 32.35 | 32.11
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1972 | 23.82 | 42.40 | 34.34
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1662 | 34.66 | 37.96 | 38.75
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1545 | 39.60 | 42.32 | 41.36
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1506 | 35.21 | 45.15 | 44.17
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1446 | 37.67 | 47.50 | 45.14
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1228 | 48.36 | 50.05 | 52.81
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1111 | 42.87 | 72.14 | 61.16
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 677 | 89.75 | 99.15 | 94.34
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 55 | 874.35 | 1348.73 | 1056.41


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3153%2C3113%2C2964%2C2904%2C2820%2C2774%2C2474%2C2159%2C1172%2C1067%2C617%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3153 | 15.53 | 24.47 | 22.57
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3113 | 16.83 | 22.91 | 21.70
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2964 | 19.71 | 23.26 | 21.76
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2904 | 20.40 | 24.73 | 22.03
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2820 | 17.45 | 28.75 | 24.99
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2774 | 20.97 | 22.91 | 23.61
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2474 | 21.17 | 29.05 | 27.53
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 2159 | 21.79 | 42.89 | 33.31
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1172 | 53.36 | 59.27 | 55.71
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1067 | 58.66 | 65.43 | 59.87
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 617 | 85.48 | 115.83 | 113.14


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3677%2C3456%2C3436%2C3012%2C2939%2C2925%2C2814%2C2804%2C2048%2C1135%2C571%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3677 | 13.91 | 19.47 | 18.78
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3456 | 15.97 | 20.80 | 19.95
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3436 | 14.43 | 21.55 | 20.02
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3012 | 16.31 | 26.26 | 23.83
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2939 | 19.21 | 23.11 | 22.57
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2925 | 18.72 | 21.68 | 22.80
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2814 | 20.13 | 25.98 | 22.97
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2804 | 18.70 | 26.39 | 24.11
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2048 | 27.58 | 32.03 | 31.56
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1135 | 55.13 | 61.41 | 56.30
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 571 | 83.47 | 170.43 | 120.58


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2915%2C2111%2C792%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2915 | 15.48 | 29.00 | 24.97
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2111 | 23.60 | 37.48 | 32.90
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 792 | 64.55 | 100.70 | 88.41


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B381%2C122%2C41%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 381 | 130.29 | 208.68 | 168.26
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 122 | 460.02 | 553.80 | 514.62
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 41 | 1050.22 | 1463.40 | 1164.83


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1917%2C1188%2C431%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1917 | 27.17 | 38.17 | 35.78
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1188 | 50.36 | 61.16 | 54.07
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 431 | 108.15 | 209.01 | 168.81


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3154%2C2819%2C669%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3154 | 15.87 | 24.48 | 21.74
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2819 | 19.40 | 26.30 | 23.99
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 669 | 64.86 | 153.90 | 109.95


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)