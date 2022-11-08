# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-11-08
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
* [The Results](#the-results-2022-11-08)
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

## The Results (2022-11-08)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5624%2C5582%2C5573%2C5391%2C5045%2C5020%2C4743%2C3623%2C2785%2C2522%2C2308%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 5624 | 12.23 | 12.58 | 11.38
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 5582 | 12.29 | 12.60 | 11.52
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5573 | 12.26 | 12.59 | 11.55
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 5391 | 12.64 | 13.07 | 11.89
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 5045 | 13.68 | 14.03 | 12.67
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 5020 | 13.43 | 13.80 | 12.81
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 4743 | 14.68 | 14.99 | 13.47
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3623 | 17.60 | 19.01 | 17.70
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 2785 | 23.39 | 25.95 | 22.97
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 2522 | 25.19 | 25.37 | 25.35
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2308 | 27.82 | 28.70 | 27.70


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4055%2C2786%2C2623%2C2158%2C2007%2C1962%2C1913%2C1820%2C1390%2C1222%2C203%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4055 | 14.18 | 18.47 | 15.77
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2786 | 21.71 | 26.65 | 22.93
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2623 | 22.44 | 28.47 | 24.40
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 2158 | 26.95 | 34.74 | 29.61
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 2007 | 29.82 | 37.55 | 31.88
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 1962 | 30.50 | 38.69 | 32.60
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 1913 | 31.08 | 39.80 | 33.40
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 1820 | 32.76 | 41.68 | 35.12
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1390 | 45.81 | 46.18 | 45.99
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1222 | 51.02 | 57.09 | 52.27
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 203 | 325.55 | 366.24 | 313.30


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5000%2C4905%2C4821%2C4575%2C4260%2C3955%2C3898%2C3310%2C2109%2C1977%2C1614%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5000 | 13.62 | 14.01 | 12.82
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 4905 | 14.04 | 14.39 | 13.03
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 4821 | 14.33 | 14.69 | 13.23
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 4575 | 15.09 | 15.46 | 13.97
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4260 | 15.54 | 16.25 | 15.15
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 3955 | 16.64 | 16.89 | 16.16
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 3898 | 17.53 | 17.96 | 16.38
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3310 | 19.08 | 21.14 | 19.32
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2109 | 30.08 | 31.84 | 30.31
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1977 | 32.33 | 32.52 | 32.33
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 1614 | 40.56 | 45.11 | 39.59


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5400%2C5355%2C5304%2C5116%2C4597%2C4469%2C4408%2C3477%2C2514%2C2410%2C2341%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 5400 | 12.58 | 12.98 | 11.83
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 5355 | 12.72 | 13.01 | 11.95
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 5304 | 12.86 | 13.18 | 12.05
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5116 | 13.28 | 13.62 | 12.54
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 4597 | 14.23 | 14.50 | 13.90
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4469 | 14.83 | 15.50 | 14.46
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 4408 | 15.45 | 15.79 | 14.49
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3477 | 18.00 | 19.95 | 18.41
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 2514 | 26.22 | 28.59 | 25.40
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 2410 | 26.42 | 26.73 | 26.54
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2341 | 27.42 | 28.18 | 27.30


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5331%2C3392%2C2181%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5331 | 12.83 | 13.16 | 12.04
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 3392 | 19.12 | 20.47 | 18.85
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 2181 | 30.71 | 33.25 | 29.30


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1466%2C150%2C81%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1466 | 40.84 | 51.79 | 43.56
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 150 | 397.38 | 500.56 | 419.20
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 81 | 708.77 | 938.50 | 764.37


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4286%2C1500%2C958%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4286 | 16.02 | 16.45 | 14.90
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 1500 | 44.79 | 47.49 | 42.61
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 958 | 70.18 | 75.00 | 66.66


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5118%2C4076%2C2592%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5118 | 13.33 | 13.64 | 12.50
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 4076 | 16.50 | 16.94 | 15.67
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 2592 | 24.87 | 28.03 | 24.66


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)