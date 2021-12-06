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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4800%2C4622%2C4081%2C4005%2C3656%2C3557%2C3504%2C3159%2C2415%2C1845%2C1716%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `` | 4800 | 11.76 | 15.41 | 13.41
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4622 | 12.37 | 16.12 | 13.88
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 4081 | 13.13 | 17.47 | 16.86
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4005 | 13.22 | 17.76 | 16.88
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3656 | 15.59 | 19.90 | 17.51
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3557 | 14.92 | 18.62 | 18.82
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 3504 | 15.09 | 21.12 | 18.96
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3159 | 18.57 | 22.61 | 20.30
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2415 | 23.82 | 30.42 | 26.53
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1845 | 26.03 | 40.97 | 35.86
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1716 | 35.96 | 40.34 | 37.25


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22blacksheep-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2958%2C2325%2C1731%2C1666%2C1664%2C1660%2C1562%2C1361%2C1242%2C1032%2C155%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `` | 2958 | 19.59 | 22.95 | 21.63
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2325 | 25.27 | 28.27 | 27.52
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 1731 | 34.72 | 37.68 | 36.92
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1666 | 35.95 | 39.81 | 38.41
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 1664 | 31.34 | 41.13 | 39.93
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1660 | 33.75 | 40.10 | 39.57
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 1562 | 38.59 | 41.52 | 40.92
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 1361 | 38.51 | 51.90 | 49.46
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1242 | 47.02 | 48.36 | 51.91
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1032 | 58.15 | 66.27 | 61.85
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 155 | 400.22 | 409.14 | 406.38


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4193%2C3879%2C3486%2C3292%2C3058%2C2857%2C2857%2C1925%2C1799%2C1624%2C1331%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `` | 4193 | 13.45 | 17.80 | 15.29
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 3879 | 14.60 | 18.93 | 16.50
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3486 | 15.45 | 20.72 | 19.19
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3292 | 17.04 | 22.22 | 19.64
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3058 | 18.43 | 22.55 | 21.41
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2857 | 20.34 | 25.13 | 22.44
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2857 | 20.61 | 25.58 | 22.46
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1925 | 27.42 | 43.20 | 33.74
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1799 | 30.11 | 34.56 | 36.83
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1624 | 38.00 | 43.23 | 39.33
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1331 | 43.19 | 56.00 | 48.03


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4301%2C4253%2C3616%2C3385%2C3288%2C3145%2C3026%2C2222%2C2184%2C2077%2C1768%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4301 | 13.27 | 16.95 | 14.87
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4253 | 13.46 | 17.20 | 15.06
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3616 | 14.32 | 19.59 | 18.76
| [squall-raw](https://pypi.org/project/python-squall/) `` | 3385 | 15.20 | 22.33 | 20.23
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3288 | 17.37 | 21.92 | 19.48
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3145 | 17.50 | 21.89 | 21.11
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3026 | 19.06 | 23.53 | 21.24
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2222 | 21.19 | 36.74 | 30.32
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2184 | 26.11 | 32.61 | 29.29
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2077 | 27.36 | 30.30 | 31.44
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1768 | 35.03 | 39.03 | 36.14


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4212%2C2854%2C2103%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `` | 4212 | 13.46 | 17.51 | 15.26
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2854 | 19.49 | 24.78 | 22.93
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2103 | 27.25 | 35.73 | 30.43


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B493%2C119%2C101%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `` | 493 | 125.31 | 132.08 | 129.71
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 119 | 496.70 | 562.04 | 532.92
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 101 | 611.13 | 618.99 | 612.55


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2507%2C1061%2C1044%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `` | 2507 | 22.92 | 29.52 | 25.52
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 1061 | 51.33 | 73.86 | 61.65
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1044 | 55.51 | 70.48 | 61.19


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22squall-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2963%2C2081%2C1970%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2963 | 18.64 | 24.42 | 22.18
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2081 | 27.34 | 34.72 | 30.73
| [squall-dataclasses](https://pypi.org/project/python-squall/) `` | 1970 | 30.21 | 41.66 | 33.22


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)