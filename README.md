# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-31
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
* [The Results](#the-results-2021-12-31)
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

## The Results (2021-12-31)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22sanic-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5439%2C5300%2C5232%2C5010%2C4707%2C4636%2C4412%2C2758%2C2238%2C1951%2C1201%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 5439 | 11.75 | 13.04 | 12.02
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5300 | 11.78 | 13.28 | 12.35
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5232 | 12.32 | 13.44 | 12.30
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5010 | 13.08 | 14.07 | 12.86
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4707 | 13.90 | 14.97 | 13.62
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4636 | 13.27 | 15.15 | 14.17
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4412 | 14.78 | 15.98 | 14.53
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2758 | 22.76 | 25.71 | 23.27
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2238 | 28.38 | 28.75 | 28.63
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1951 | 31.36 | 34.11 | 32.75
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 1201 | 55.19 | 56.88 | 53.20


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3682%2C2632%2C2202%2C1784%2C1663%2C1594%2C1579%2C1270%2C1030%2C967%2C218%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 3682 | 16.72 | 19.71 | 17.50
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2632 | 22.20 | 28.18 | 24.28
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2202 | 27.44 | 32.66 | 29.03
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1784 | 33.50 | 42.05 | 35.79
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1663 | 36.59 | 45.13 | 38.41
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1594 | 38.54 | 46.49 | 40.06
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1579 | 38.29 | 46.80 | 40.45
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1270 | 50.04 | 50.42 | 50.32
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1030 | 62.18 | 66.77 | 62.05
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 967 | 61.13 | 77.72 | 66.04
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 218 | 288.31 | 342.64 | 291.23


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%2C%22sanic-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4836%2C4578%2C4463%2C4321%2C3858%2C3530%2C3432%2C1928%2C1771%2C1601%2C1180%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4836 | 13.04 | 14.59 | 13.47
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4578 | 14.22 | 15.41 | 14.02
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4463 | 14.70 | 15.88 | 14.33
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4321 | 14.71 | 16.30 | 14.96
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3858 | 15.80 | 17.74 | 17.15
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3530 | 17.95 | 19.44 | 18.10
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3432 | 18.57 | 19.16 | 18.61
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1928 | 32.88 | 33.60 | 33.15
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1771 | 34.43 | 38.45 | 36.07
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1601 | 39.05 | 44.36 | 39.87
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 1180 | 56.24 | 58.09 | 54.12


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22sanic-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5061%2C4999%2C4963%2C4924%2C4073%2C4012%2C3954%2C2389%2C2381%2C2001%2C1211%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5061 | 12.83 | 13.79 | 12.66
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4999 | 12.64 | 14.13 | 13.03
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4963 | 12.67 | 14.06 | 13.09
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4924 | 13.04 | 14.17 | 13.05
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4073 | 14.93 | 16.75 | 16.23
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4012 | 15.90 | 16.40 | 15.93
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3954 | 15.83 | 17.22 | 16.22
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2389 | 25.57 | 29.96 | 26.77
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2381 | 26.65 | 27.05 | 26.84
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2001 | 29.98 | 33.98 | 31.93
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 1211 | 54.28 | 56.11 | 52.73


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5205%2C3368%2C2398%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 5205 | 12.12 | 13.67 | 12.55
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3368 | 18.67 | 20.28 | 19.03
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2398 | 26.36 | 29.15 | 26.70


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1471%2C202%2C139%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 1471 | 42.93 | 49.28 | 43.42
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 202 | 324.43 | 345.20 | 313.89
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 139 | 452.47 | 534.40 | 457.37


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4231%2C1640%2C1179%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4231 | 15.11 | 16.76 | 15.21
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1640 | 38.58 | 43.41 | 38.95
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1179 | 53.57 | 60.72 | 54.17


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4981%2C3907%2C2259%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4981 | 12.76 | 14.14 | 13.03
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3907 | 15.80 | 17.87 | 16.44
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2259 | 26.90 | 31.66 | 28.28


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)