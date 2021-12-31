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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22sanic-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5233%2C5164%2C5142%2C5083%2C4739%2C4530%2C4462%2C2810%2C2183%2C1997%2C1222%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5233 | 12.61 | 13.55 | 12.28
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5164 | 12.64 | 13.59 | 12.57
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5142 | 12.56 | 13.60 | 12.64
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5083 | 12.88 | 13.91 | 12.66
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4739 | 13.95 | 15.00 | 13.50
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4530 | 14.24 | 15.56 | 14.37
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4462 | 14.68 | 15.82 | 14.35
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2810 | 22.32 | 25.54 | 22.78
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2183 | 28.98 | 29.25 | 29.29
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1997 | 30.60 | 33.17 | 32.02
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 1222 | 54.17 | 56.06 | 52.30


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3562%2C2665%2C2104%2C1838%2C1653%2C1636%2C1568%2C1231%2C1063%2C977%2C216%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3562 | 17.21 | 20.04 | 17.99
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2665 | 22.07 | 27.76 | 23.95
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2104 | 27.52 | 35.40 | 30.38
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1838 | 32.40 | 41.02 | 34.75
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1653 | 36.35 | 44.98 | 38.69
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1636 | 37.68 | 45.79 | 39.06
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1568 | 38.32 | 47.83 | 40.75
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1231 | 51.64 | 52.01 | 51.90
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1063 | 60.59 | 64.83 | 60.08
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 977 | 60.64 | 77.04 | 65.27
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 216 | 290.61 | 343.09 | 294.05


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%2C%22sanic-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4618%2C4577%2C4504%2C4221%2C3744%2C3590%2C3468%2C1935%2C1803%2C1621%2C1211%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4618 | 14.04 | 15.10 | 14.01
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4577 | 14.35 | 15.47 | 14.01
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4504 | 14.55 | 15.78 | 14.21
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4221 | 15.35 | 16.55 | 15.24
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3744 | 16.58 | 18.02 | 17.55
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3590 | 17.71 | 19.13 | 17.80
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3468 | 18.43 | 19.00 | 18.42
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1935 | 32.87 | 33.23 | 33.03
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1803 | 33.88 | 37.60 | 35.45
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1621 | 38.89 | 44.07 | 39.41
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 1211 | 54.72 | 56.30 | 52.76


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22sanic-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5077%2C4949%2C4883%2C4704%2C4121%2C4087%2C3980%2C2467%2C2413%2C2062%2C1230%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5077 | 12.96 | 13.82 | 12.61
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4949 | 13.14 | 14.16 | 12.97
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4883 | 13.15 | 14.26 | 13.25
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4704 | 13.62 | 14.73 | 13.75
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4121 | 15.48 | 16.74 | 15.54
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4087 | 15.65 | 16.16 | 15.66
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3980 | 15.80 | 17.16 | 16.52
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2467 | 25.17 | 28.60 | 25.92
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2413 | 26.21 | 26.52 | 26.50
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2062 | 29.18 | 31.62 | 30.99
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.0` | 1230 | 53.51 | 55.29 | 51.93


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4924%2C3527%2C2450%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4924 | 13.17 | 14.24 | 13.15
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3527 | 17.93 | 19.33 | 18.13
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2450 | 25.89 | 28.54 | 26.10


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1419%2C183%2C140%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1419 | 43.34 | 51.80 | 45.01
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 183 | 333.80 | 389.07 | 344.58
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 140 | 443.31 | 521.43 | 453.33


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3945%2C1653%2C1216%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 3945 | 16.45 | 17.63 | 16.28
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1653 | 39.75 | 42.14 | 38.64
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1216 | 52.73 | 57.72 | 52.54


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4697%2C3822%2C2302%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4697 | 13.83 | 14.89 | 13.74
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3822 | 16.58 | 17.86 | 16.77
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2302 | 26.59 | 31.03 | 27.76


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)