# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-10-31
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
* [The Results](#the-results-2022-10-31)
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

## The Results (2022-10-31)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5111%2C5109%2C5086%2C4933%2C4583%2C4389%2C4277%2C3417%2C2662%2C2154%2C2020%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 5111 | 12.57 | 13.65 | 12.62
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 5109 | 12.55 | 13.61 | 12.69
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5086 | 12.65 | 13.61 | 12.76
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4933 | 13.05 | 14.22 | 13.05
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 4583 | 14.23 | 15.24 | 14.00
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4389 | 14.31 | 15.59 | 14.84
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 4277 | 15.01 | 16.25 | 14.97
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 3417 | 17.79 | 20.24 | 18.92
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2662 | 23.10 | 26.82 | 24.08
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2154 | 29.20 | 29.72 | 29.68
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2020 | 29.93 | 33.15 | 31.64


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3252%2C2487%2C2148%2C1840%2C1770%2C1643%2C1619%2C1576%2C1224%2C1066%2C206%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3252 | 17.07 | 23.00 | 19.69
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2487 | 23.56 | 29.89 | 25.70
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2148 | 27.21 | 34.03 | 29.79
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 1840 | 31.75 | 39.50 | 34.72
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1770 | 33.39 | 42.33 | 36.10
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 1643 | 35.92 | 45.36 | 38.84
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 1619 | 36.81 | 46.50 | 39.46
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1576 | 38.25 | 47.02 | 40.52
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1224 | 51.92 | 52.48 | 52.21
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1066 | 59.55 | 64.75 | 59.93
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 206 | 307.65 | 356.26 | 307.71


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4585%2C4519%2C4339%2C4152%2C3703%2C3477%2C3439%2C2981%2C1882%2C1804%2C1506%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4585 | 14.14 | 15.18 | 14.07
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 4519 | 14.33 | 15.55 | 14.18
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4339 | 14.90 | 16.13 | 14.73
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 4152 | 15.43 | 16.68 | 15.49
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3703 | 16.72 | 18.12 | 17.73
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3477 | 18.10 | 19.73 | 18.37
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 3439 | 18.54 | 19.14 | 18.58
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 2981 | 20.10 | 23.93 | 21.65
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1882 | 33.67 | 34.09 | 33.99
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1804 | 33.55 | 37.99 | 35.44
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1506 | 41.51 | 48.23 | 42.40


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4887%2C4819%2C4790%2C4636%2C3982%2C3891%2C3787%2C3180%2C2337%2C2314%2C2028%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4887 | 13.11 | 14.16 | 13.12
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 4819 | 13.28 | 14.42 | 13.33
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 4790 | 13.29 | 14.37 | 13.49
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4636 | 13.86 | 14.91 | 13.93
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 3982 | 15.91 | 16.50 | 16.05
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3891 | 16.12 | 17.50 | 16.45
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3787 | 15.99 | 17.68 | 17.38
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.2` | 3180 | 18.79 | 22.43 | 20.34
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2337 | 26.51 | 30.78 | 27.41
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2314 | 27.23 | 28.02 | 27.64
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2028 | 29.68 | 33.01 | 31.51


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4863%2C2983%2C2074%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4863 | 13.22 | 14.27 | 13.28
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 2983 | 20.83 | 23.71 | 21.48
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2074 | 30.30 | 33.86 | 30.81


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1370%2C150%2C83%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1370 | 43.45 | 54.39 | 46.62
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 150 | 436.76 | 487.47 | 422.14
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 83 | 732.67 | 876.44 | 754.37


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3831%2C1284%2C888%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 3831 | 16.75 | 17.89 | 16.70
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 1284 | 49.17 | 54.88 | 49.75
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 888 | 72.32 | 79.51 | 71.92


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4680%2C3468%2C2426%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4680 | 13.83 | 14.86 | 13.74
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 3468 | 17.72 | 19.68 | 18.50
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2426 | 25.58 | 29.94 | 26.34


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)