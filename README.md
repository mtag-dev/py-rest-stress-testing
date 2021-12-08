# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-08
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
* [The Results](#the-results-2021-12-08)
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

## The Results (2021-12-08)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5843%2C5603%2C5454%2C5192%2C4893%2C4861%2C4430%2C3993%2C3044%2C2153%2C1989%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 5843 | 10.79 | 11.93 | 11.17
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5603 | 11.45 | 12.50 | 11.54
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 5454 | 11.47 | 12.84 | 12.01
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 5192 | 12.07 | 13.57 | 12.51
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 4893 | 13.00 | 14.59 | 13.14
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 4861 | 13.28 | 14.42 | 13.20
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4430 | 14.03 | 15.80 | 14.90
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3993 | 15.67 | 17.13 | 16.24
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 3044 | 20.11 | 22.89 | 21.15
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2153 | 29.36 | 29.84 | 29.68
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1989 | 30.00 | 33.17 | 32.16


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4170%2C2624%2C2197%2C2082%2C2023%2C1779%2C1639%2C1620%2C1208%2C1037%2C230%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4170 | 14.29 | 17.45 | 15.45
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2624 | 22.63 | 27.74 | 24.36
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2197 | 27.89 | 32.67 | 29.10
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2082 | 28.23 | 36.03 | 30.70
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2023 | 29.70 | 36.89 | 31.58
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 1779 | 34.31 | 41.36 | 35.90
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 1639 | 36.55 | 45.27 | 39.00
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1620 | 38.35 | 46.52 | 39.43
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1208 | 52.66 | 53.85 | 52.90
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1037 | 60.19 | 66.63 | 61.65
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 230 | 278.64 | 332.15 | 276.07


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5103%2C4920%2C4605%2C4534%2C3760%2C3736%2C3567%2C3532%2C1980%2C1881%2C1570%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 5103 | 12.36 | 13.72 | 12.77
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4920 | 13.13 | 14.40 | 13.02
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4605 | 13.84 | 15.34 | 14.02
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 4534 | 14.09 | 15.34 | 14.32
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3760 | 16.07 | 18.25 | 17.65
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3736 | 16.92 | 18.82 | 17.11
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3567 | 16.90 | 19.10 | 18.24
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 3532 | 18.11 | 19.16 | 18.12
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1980 | 30.39 | 33.91 | 32.27
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1881 | 33.65 | 35.09 | 33.99
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1570 | 39.18 | 45.31 | 40.68


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5372%2C5309%2C5221%2C4927%2C4322%2C4200%2C3961%2C3711%2C2425%2C2295%2C2229%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 5372 | 11.74 | 12.81 | 12.14
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5309 | 11.92 | 13.40 | 12.11
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 5221 | 12.01 | 13.32 | 12.49
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4927 | 12.84 | 14.30 | 13.14
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 4322 | 14.64 | 16.35 | 14.86
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 4200 | 15.07 | 16.02 | 15.23
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3961 | 15.33 | 17.18 | 16.80
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3711 | 16.17 | 18.37 | 17.61
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2425 | 26.47 | 27.15 | 26.37
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2295 | 26.50 | 31.67 | 27.98
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 2229 | 27.03 | 29.18 | 28.67


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5457%2C3891%2C2434%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 5457 | 11.61 | 12.77 | 11.88
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 3891 | 16.30 | 17.60 | 16.50
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2434 | 25.48 | 29.31 | 26.36


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B868%2C208%2C148%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 868 | 75.64 | 83.65 | 73.54
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 208 | 318.32 | 352.92 | 304.75
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 148 | 412.63 | 499.79 | 422.65


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3349%2C1683%2C1162%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 3349 | 17.80 | 20.37 | 19.12
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 1683 | 37.76 | 42.18 | 37.95
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1162 | 53.58 | 62.07 | 54.93


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5262%2C3990%2C2197%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 5262 | 12.07 | 13.15 | 12.31
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 3990 | 15.38 | 17.48 | 16.14
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2197 | 27.35 | 32.91 | 29.15


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)