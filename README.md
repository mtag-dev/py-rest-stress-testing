# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-12
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
* [The Results](#the-results-2021-12-12)
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

## The Results (2021-12-12)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5400%2C5197%2C5031%2C5016%2C4619%2C4459%2C4416%2C3744%2C2757%2C2181%2C1947%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 5400 | 11.95 | 12.91 | 12.06
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 5197 | 12.42 | 13.43 | 12.40
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5031 | 12.81 | 13.84 | 12.95
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5016 | 12.87 | 13.93 | 12.84
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4619 | 14.11 | 15.18 | 13.88
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4459 | 14.30 | 15.68 | 14.63
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4416 | 14.60 | 15.76 | 14.51
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3744 | 16.62 | 18.25 | 17.20
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2757 | 22.82 | 25.78 | 23.26
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2181 | 29.01 | 29.30 | 29.31
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1947 | 31.62 | 34.61 | 32.81


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3476%2C2660%2C2028%2C1987%2C1788%2C1634%2C1599%2C1529%2C1221%2C1033%2C216%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 3476 | 17.13 | 20.74 | 18.46
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 2660 | 22.11 | 27.82 | 24.07
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2028 | 28.70 | 36.30 | 31.50
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 1987 | 30.07 | 36.72 | 32.15
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1788 | 33.07 | 41.77 | 35.73
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1634 | 36.60 | 45.50 | 39.09
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1599 | 38.61 | 46.49 | 39.95
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1529 | 39.19 | 48.15 | 41.77
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1221 | 51.72 | 52.44 | 52.36
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1033 | 61.89 | 67.08 | 61.87
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 216 | 292.19 | 344.23 | 293.21


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4745%2C4607%2C4484%2C4182%2C3713%2C3496%2C3411%2C3255%2C1870%2C1736%2C1534%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4745 | 13.40 | 14.60 | 13.63
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 4607 | 14.23 | 15.31 | 13.91
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4484 | 14.59 | 15.68 | 14.26
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4182 | 15.42 | 16.66 | 15.36
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3713 | 16.57 | 18.33 | 17.61
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3496 | 17.96 | 19.60 | 18.29
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3411 | 18.56 | 19.19 | 18.73
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3255 | 18.48 | 21.71 | 19.80
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1870 | 33.72 | 34.30 | 34.19
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1736 | 35.35 | 39.52 | 36.79
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1534 | 40.78 | 47.16 | 41.63


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5068%2C4896%2C4838%2C4824%2C4038%2C3975%2C3893%2C3415%2C2337%2C2322%2C1993%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5068 | 12.86 | 13.79 | 12.64
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4896 | 13.07 | 14.16 | 13.22
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4838 | 13.24 | 14.25 | 13.39
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 4824 | 13.30 | 14.40 | 13.35
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4038 | 15.69 | 16.24 | 15.82
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3975 | 15.77 | 17.34 | 16.12
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3893 | 15.88 | 17.39 | 16.88
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3415 | 17.45 | 20.65 | 19.01
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2337 | 26.82 | 27.57 | 27.36
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2322 | 26.38 | 31.23 | 27.53
| [quart-raw](https://pypi.org/project/quart/) `0.16.1` | 1993 | 30.14 | 34.36 | 32.07


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4946%2C3452%2C2381%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4946 | 13.04 | 14.12 | 13.06
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3452 | 18.21 | 19.75 | 18.56
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2381 | 26.46 | 29.73 | 26.84


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B789%2C180%2C139%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 789 | 77.41 | 94.22 | 80.91
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 180 | 342.89 | 414.48 | 354.04
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 139 | 446.27 | 526.41 | 454.63


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2967%2C1610%2C1167%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 2967 | 20.15 | 24.43 | 21.56
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1610 | 40.41 | 43.38 | 39.66
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1167 | 54.77 | 61.90 | 54.76


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4738%2C3757%2C2253%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4738 | 13.51 | 14.61 | 13.60
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3757 | 16.63 | 18.13 | 17.05
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2253 | 27.15 | 31.83 | 28.36


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)