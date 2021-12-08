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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4802%2C4646%2C4478%2C4432%2C4053%2C3830%2C3733%2C3164%2C2429%2C1854%2C1725%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4802 | 13.31 | 14.46 | 13.47
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4646 | 13.76 | 14.96 | 13.81
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 4478 | 14.34 | 15.57 | 14.47
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4432 | 14.60 | 15.78 | 14.50
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 4053 | 15.90 | 17.20 | 15.78
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3830 | 16.76 | 18.02 | 16.94
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3733 | 16.72 | 18.05 | 17.14
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3164 | 19.35 | 22.04 | 20.27
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2429 | 25.70 | 29.25 | 26.36
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1854 | 34.00 | 34.47 | 34.47
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1725 | 35.84 | 39.62 | 37.05


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3061%2C2334%2C1777%2C1739%2C1532%2C1402%2C1364%2C1295%2C1057%2C921%2C187%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 3061 | 19.57 | 23.76 | 20.91
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2334 | 25.96 | 31.50 | 27.38
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 1777 | 33.57 | 41.84 | 35.96
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 1739 | 33.85 | 42.67 | 36.74
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1532 | 39.40 | 48.40 | 41.70
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 1402 | 43.62 | 52.07 | 45.51
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1364 | 45.74 | 54.18 | 46.81
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 1295 | 46.41 | 57.90 | 49.31
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1057 | 60.58 | 61.01 | 60.58
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 921 | 69.53 | 74.76 | 69.33
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 187 | 355.52 | 376.92 | 341.31


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4240%2C3985%2C3838%2C3428%2C3074%2C2975%2C2817%2C2727%2C1649%2C1565%2C1365%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4240 | 15.12 | 16.45 | 15.19
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 3985 | 16.16 | 17.53 | 16.04
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3838 | 16.64 | 18.03 | 16.65
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3428 | 18.01 | 19.84 | 18.72
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3074 | 19.49 | 23.08 | 21.10
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2975 | 21.36 | 22.13 | 21.47
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2817 | 21.72 | 25.38 | 22.67
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2727 | 21.88 | 26.51 | 23.52
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1649 | 38.63 | 39.04 | 38.76
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1565 | 39.30 | 43.81 | 40.84
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1365 | 46.07 | 51.73 | 46.77


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4399%2C4366%2C4323%2C4263%2C3514%2C3355%2C3265%2C2914%2C2060%2C2054%2C1754%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4399 | 14.71 | 15.88 | 14.57
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4366 | 14.73 | 15.90 | 14.66
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4323 | 14.79 | 16.04 | 14.91
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 4263 | 14.92 | 16.22 | 15.10
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 3514 | 18.10 | 18.76 | 18.18
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3355 | 18.26 | 20.82 | 19.04
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3265 | 18.15 | 21.46 | 19.96
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2914 | 20.37 | 24.68 | 22.04
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2060 | 30.78 | 31.19 | 31.02
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2054 | 29.61 | 34.66 | 31.10
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1754 | 34.76 | 39.55 | 36.42


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4375%2C2871%2C2066%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 4375 | 14.75 | 15.93 | 14.71
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2871 | 21.58 | 24.85 | 22.24
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2066 | 30.05 | 33.99 | 30.93


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B687%2C159%2C119%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 687 | 95.25 | 105.04 | 92.79
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 159 | 422.72 | 446.72 | 397.36
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 119 | 534.49 | 598.53 | 526.07


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2530%2C1359%2C1033%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2530 | 23.63 | 29.21 | 25.26
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 1359 | 47.18 | 51.19 | 46.95
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1033 | 61.50 | 68.70 | 61.84


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4227%2C3168%2C1957%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 4227 | 15.15 | 16.43 | 15.17
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 3168 | 19.21 | 22.18 | 20.15
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1957 | 31.37 | 36.66 | 32.64


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)