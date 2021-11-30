# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-30
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
* [The Results](#the-results-2021-11-30)
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

## The Results (2021-11-30)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4958%2C4784%2C4723%2C4591%2C4438%2C4142%2C3934%2C3470%2C2523%2C2271%2C1847%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4958 | 11.63 | 14.40 | 12.96
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4784 | 12.12 | 15.57 | 13.38
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4723 | 12.10 | 15.37 | 13.61
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4591 | 12.51 | 16.01 | 13.98
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4438 | 13.15 | 16.75 | 14.40
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4142 | 13.85 | 15.48 | 15.56
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3934 | 14.64 | 18.81 | 16.27
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3470 | 16.52 | 20.77 | 18.48
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2523 | 23.30 | 28.84 | 25.39
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2271 | 25.74 | 28.26 | 28.30
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1847 | 33.40 | 37.41 | 34.62


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3162%2C2411%2C2060%2C1835%2C1828%2C1741%2C1737%2C1623%2C1295%2C1108%2C162%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3162 | 18.38 | 21.39 | 20.23
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2411 | 24.61 | 27.78 | 26.52
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2060 | 29.20 | 31.70 | 31.05
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1835 | 32.73 | 35.76 | 34.85
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1828 | 32.87 | 35.73 | 34.97
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1741 | 34.33 | 36.79 | 36.75
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1737 | 34.27 | 37.80 | 36.83
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1623 | 37.57 | 39.70 | 39.41
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1295 | 46.77 | 48.51 | 49.91
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1108 | 54.31 | 59.62 | 57.66
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 162 | 380.93 | 389.79 | 390.05


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4316%2C4132%2C3980%2C3763%2C3204%2C3152%2C3077%2C3049%2C2067%2C1679%2C1383%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4316 | 13.37 | 17.23 | 14.85
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4132 | 13.94 | 18.24 | 15.48
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3980 | 14.93 | 18.42 | 16.06
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3763 | 15.57 | 19.45 | 17.03
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3204 | 18.40 | 21.76 | 20.14
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3152 | 19.94 | 21.08 | 20.28
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3077 | 18.95 | 23.01 | 20.86
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3049 | 19.56 | 23.90 | 20.97
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2067 | 30.03 | 31.57 | 30.94
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1679 | 36.42 | 41.33 | 38.09
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1383 | 41.22 | 54.71 | 46.32


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4459%2C4424%2C4404%2C4374%2C3512%2C3509%2C3325%2C3279%2C2305%2C2289%2C1834%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4459 | 13.18 | 16.05 | 14.34
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 4424 | 13.20 | 16.48 | 14.50
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4404 | 13.14 | 16.57 | 14.52
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4374 | 12.99 | 16.54 | 14.69
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3512 | 17.74 | 19.18 | 18.20
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3509 | 16.77 | 20.44 | 18.23
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3325 | 17.32 | 21.11 | 19.47
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3279 | 17.81 | 21.64 | 19.61
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2305 | 27.16 | 27.92 | 27.73
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2289 | 25.00 | 31.63 | 27.95
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1834 | 33.45 | 37.80 | 34.86


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3915%2C3182%2C2161%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3915 | 14.68 | 18.33 | 16.37
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3182 | 18.10 | 22.19 | 20.10
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2161 | 26.78 | 34.35 | 29.59


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B495%2C139%2C97%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 495 | 124.71 | 126.92 | 128.41
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 139 | 439.82 | 451.77 | 455.95
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 97 | 619.25 | 654.24 | 640.03


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2355%2C1429%2C1099%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2355 | 24.56 | 31.31 | 27.15
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1429 | 40.92 | 51.70 | 44.75
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1099 | 52.71 | 68.72 | 58.18


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4069%2C3459%2C2186%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 4069 | 13.97 | 18.24 | 15.75
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3459 | 16.79 | 20.54 | 18.49
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2186 | 26.48 | 33.06 | 29.28


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)