# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-10-30
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
* [The Results](#the-results-2022-10-30)
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

## The Results (2022-10-30)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5357%2C5294%2C5234%2C5099%2C4878%2C4624%2C4541%2C3576%2C2837%2C2280%2C2092%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5357 | 11.94 | 13.20 | 12.04
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5294 | 12.14 | 13.23 | 12.25
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 5234 | 12.23 | 13.30 | 12.44
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5099 | 12.70 | 13.73 | 12.63
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4878 | 13.19 | 14.36 | 13.16
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4624 | 13.59 | 14.74 | 14.12
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 4541 | 14.24 | 15.45 | 14.10
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3576 | 16.92 | 19.29 | 18.13
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2837 | 21.83 | 25.27 | 22.60
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2280 | 28.09 | 28.47 | 28.04
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2092 | 28.46 | 31.50 | 30.72


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3434%2C2590%2C2343%2C2025%2C1926%2C1746%2C1663%2C1594%2C1239%2C1126%2C212%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3434 | 16.11 | 21.72 | 18.65
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2590 | 22.36 | 28.85 | 24.71
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2343 | 24.70 | 31.72 | 27.31
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2025 | 28.56 | 36.69 | 31.59
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1926 | 30.70 | 39.35 | 33.18
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 1746 | 33.96 | 43.53 | 36.59
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1663 | 35.64 | 45.28 | 38.76
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1594 | 36.99 | 47.32 | 40.06
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1239 | 50.08 | 51.04 | 51.79
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1126 | 55.66 | 61.58 | 56.80
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 212 | 299.89 | 341.75 | 296.61


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4751%2C4672%2C4361%2C4264%2C3879%2C3678%2C3516%2C3170%2C1924%2C1687%2C1581%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4751 | 13.54 | 14.65 | 13.59
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4672 | 13.84 | 15.00 | 13.73
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 4361 | 14.88 | 16.14 | 14.75
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4264 | 14.47 | 15.86 | 15.30
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3879 | 15.90 | 17.53 | 16.92
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3678 | 17.30 | 18.66 | 17.37
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3516 | 17.77 | 18.44 | 18.33
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3170 | 19.11 | 22.33 | 20.41
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1924 | 31.70 | 35.63 | 33.20
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1687 | 32.48 | 33.57 | 37.95
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1581 | 39.55 | 45.51 | 40.69


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5174%2C5067%2C4970%2C4794%2C4156%2C4111%2C3913%2C3417%2C2466%2C2431%2C2199%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5174 | 12.52 | 13.48 | 12.38
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 5067 | 12.52 | 13.72 | 12.77
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4970 | 12.97 | 14.00 | 12.93
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4794 | 13.20 | 14.31 | 13.53
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4156 | 15.28 | 15.77 | 15.39
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 4111 | 15.21 | 16.58 | 15.58
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3913 | 15.35 | 17.13 | 16.84
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3417 | 17.51 | 20.66 | 19.00
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2466 | 25.39 | 26.14 | 25.94
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2431 | 25.70 | 29.70 | 26.29
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2199 | 27.60 | 30.60 | 29.06


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5045%2C3174%2C2135%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5045 | 12.69 | 13.91 | 12.80
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 3174 | 19.14 | 22.06 | 20.33
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2135 | 29.26 | 32.28 | 30.18


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1388%2C156%2C84%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1388 | 42.00 | 54.07 | 46.43
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 156 | 396.34 | 467.75 | 405.18
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 84 | 697.90 | 869.55 | 738.66


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4051%2C1398%2C909%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4051 | 15.85 | 17.18 | 15.83
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 1398 | 44.94 | 51.02 | 45.77
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 909 | 71.25 | 77.28 | 70.20


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4824%2C3748%2C2525%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4824 | 13.24 | 14.43 | 13.34
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 3748 | 16.68 | 18.14 | 17.08
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2525 | 24.63 | 28.65 | 25.32


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)