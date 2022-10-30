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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5303%2C5270%2C5210%2C5147%2C4814%2C4675%2C4554%2C3675%2C2821%2C2218%2C2149%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5303 | 12.04 | 13.04 | 12.14
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5270 | 12.11 | 13.18 | 12.28
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 5210 | 12.23 | 13.36 | 12.40
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5147 | 12.47 | 13.55 | 12.49
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4814 | 13.48 | 14.60 | 13.30
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4675 | 13.74 | 14.73 | 13.90
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 4554 | 14.27 | 15.41 | 14.05
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3675 | 16.71 | 18.62 | 17.52
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2821 | 22.10 | 25.54 | 22.69
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2218 | 28.53 | 28.70 | 28.82
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2149 | 28.33 | 30.74 | 29.72


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3556%2C2655%2C2347%2C2025%2C1916%2C1730%2C1688%2C1642%2C1263%2C1137%2C210%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3556 | 15.55 | 21.03 | 18.00
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2655 | 21.63 | 28.38 | 24.07
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2347 | 24.50 | 31.80 | 27.24
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2025 | 28.32 | 36.52 | 32.02
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1916 | 30.60 | 40.01 | 33.35
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 1730 | 34.15 | 43.94 | 36.93
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1688 | 35.03 | 45.09 | 37.83
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1642 | 36.12 | 46.32 | 38.91
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1263 | 50.46 | 50.74 | 50.57
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1137 | 57.14 | 60.89 | 56.20
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 210 | 328.12 | 347.74 | 301.10


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4745%2C4627%2C4622%2C4298%2C3928%2C3647%2C3533%2C3302%2C1956%2C1930%2C1608%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4745 | 13.62 | 14.65 | 13.56
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4627 | 14.03 | 15.20 | 13.83
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4622 | 13.94 | 15.16 | 13.86
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 4298 | 14.93 | 16.20 | 14.91
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3928 | 16.02 | 17.32 | 16.59
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3647 | 17.27 | 18.75 | 17.51
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3533 | 18.08 | 18.60 | 18.08
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3302 | 18.58 | 20.85 | 19.50
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1956 | 32.55 | 32.80 | 32.68
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1930 | 31.66 | 35.38 | 33.13
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1608 | 39.48 | 44.17 | 39.74


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5174%2C5045%2C4998%2C4830%2C4150%2C4114%2C4113%2C3472%2C2466%2C2447%2C2157%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5174 | 12.42 | 13.39 | 12.37
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5045 | 12.75 | 13.79 | 12.71
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 4998 | 12.71 | 13.85 | 12.90
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4830 | 13.14 | 14.27 | 13.34
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 4150 | 15.19 | 16.42 | 15.40
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4114 | 15.46 | 15.91 | 15.53
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4113 | 15.19 | 16.44 | 15.88
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3472 | 17.46 | 20.11 | 18.55
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2466 | 25.61 | 26.02 | 25.93
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2447 | 25.69 | 29.05 | 26.14
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2157 | 28.23 | 30.89 | 29.61


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5027%2C3098%2C2161%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5027 | 12.80 | 13.88 | 12.82
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 3098 | 20.05 | 22.30 | 20.67
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2161 | 29.25 | 32.40 | 29.57


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1424%2C155%2C84%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1424 | 40.98 | 53.70 | 44.82
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 155 | 411.81 | 473.69 | 408.95
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 84 | 693.35 | 883.74 | 738.07


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4029%2C1342%2C923%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4029 | 15.98 | 17.13 | 15.86
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 1342 | 47.23 | 52.55 | 47.65
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 923 | 70.25 | 75.26 | 69.18


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4812%2C3730%2C2545%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4812 | 13.35 | 14.39 | 13.32
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 3730 | 16.77 | 18.21 | 17.13
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2545 | 24.56 | 28.62 | 25.09


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)