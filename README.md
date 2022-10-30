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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3089%2C3017%2C3003%2C2844%2C2598%2C2563%2C2515%2C2091%2C1747%2C1454%2C1286%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 3089 | 19.11 | 23.65 | 20.70
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3017 | 19.66 | 24.40 | 21.21
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3003 | 19.80 | 24.48 | 21.27
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 2844 | 20.65 | 26.24 | 22.54
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 2598 | 22.65 | 28.76 | 24.61
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2563 | 23.02 | 28.99 | 24.98
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2515 | 23.88 | 29.72 | 25.43
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 2091 | 29.12 | 35.13 | 30.61
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1747 | 35.05 | 42.18 | 36.57
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1454 | 42.80 | 45.28 | 43.99
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1286 | 48.25 | 54.28 | 49.70


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2289%2C1754%2C1569%2C1317%2C1284%2C1203%2C1174%2C1127%2C893%2C797%2C159%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2289 | 26.22 | 31.89 | 27.93
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 1754 | 35.06 | 41.51 | 36.44
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 1569 | 38.83 | 46.20 | 40.72
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 1317 | 46.64 | 56.34 | 48.53
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1284 | 47.70 | 56.70 | 49.78
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 1203 | 50.97 | 61.39 | 53.14
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 1174 | 52.15 | 62.84 | 54.41
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1127 | 53.86 | 65.47 | 56.65
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 893 | 70.62 | 74.43 | 71.61
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 797 | 79.22 | 87.89 | 80.15
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 159 | 385.35 | 461.67 | 395.04


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2644%2C2583%2C2522%2C2289%2C2280%2C2126%2C2097%2C1839%2C1302%2C1244%2C1027%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2644 | 22.70 | 28.26 | 24.15
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2583 | 23.35 | 29.12 | 24.72
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2522 | 23.65 | 29.60 | 25.34
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 2289 | 27.07 | 29.23 | 27.90
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 2280 | 26.52 | 32.86 | 28.03
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2126 | 29.40 | 34.63 | 30.04
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2097 | 28.54 | 35.10 | 30.90
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 1839 | 32.85 | 40.49 | 34.74
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1302 | 48.45 | 51.28 | 49.09
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1244 | 50.06 | 56.19 | 51.33
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1027 | 61.57 | 70.92 | 62.81


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3020%2C2810%2C2691%2C2675%2C2659%2C2299%2C2227%2C2009%2C1586%2C1518%2C1341%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3020 | 19.68 | 24.36 | 21.15
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2810 | 21.29 | 26.29 | 22.73
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 2691 | 22.03 | 27.77 | 23.75
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 2675 | 23.07 | 25.15 | 23.88
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2659 | 22.39 | 28.02 | 24.03
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2299 | 26.70 | 32.50 | 27.79
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2227 | 27.06 | 33.29 | 28.80
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 2009 | 30.36 | 36.90 | 31.81
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1586 | 39.70 | 41.81 | 40.32
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1518 | 40.16 | 48.70 | 42.10
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1341 | 46.38 | 52.06 | 47.66


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2716%2C1980%2C1338%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2716 | 21.73 | 27.40 | 23.60
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 1980 | 31.33 | 36.88 | 32.29
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 1338 | 46.84 | 54.78 | 47.75


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1009%2C113%2C65%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1009 | 59.94 | 72.91 | 63.23
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 113 | 531.70 | 671.55 | 557.05
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 65 | 864.05 | 1172.26 | 953.41


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2249%2C872%2C647%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2249 | 27.38 | 32.81 | 28.41
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 872 | 71.83 | 83.23 | 73.14
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 647 | 98.73 | 109.90 | 98.55


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2591%2C2074%2C1541%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2591 | 22.99 | 29.04 | 24.66
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 2074 | 29.65 | 35.75 | 30.93
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 1541 | 39.31 | 48.12 | 41.40


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)