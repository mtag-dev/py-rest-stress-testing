# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-06
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
* [The Results](#the-results-2021-12-06)
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

## The Results (2021-12-06)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22muffin-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4196%2C4088%2C3597%2C3296%2C2851%2C1965%2C1831%2C1742%2C1582%2C1509%2C1124%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4196 | 13.14 | 17.13 | 15.65
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4088 | 13.11 | 17.56 | 16.87
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3597 | 15.26 | 19.84 | 18.66
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3296 | 15.46 | 21.05 | 21.35
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2851 | 23.09 | 28.92 | 22.73
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1965 | 26.55 | 37.02 | 35.29
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1831 | 26.38 | 37.06 | 39.18
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1742 | 30.02 | 44.93 | 37.20
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1582 | 33.59 | 47.90 | 40.96
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1509 | 36.74 | 47.03 | 43.60
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1124 | 44.28 | 70.78 | 58.91


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22starlette-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1594%2C1593%2C1573%2C1551%2C1520%2C1443%2C920%2C899%2C687%2C543%2C141%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1594 | 37.40 | 40.58 | 40.13
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 1593 | 32.47 | 44.94 | 42.12
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1573 | 35.07 | 43.31 | 41.84
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1551 | 37.79 | 42.48 | 41.24
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 1520 | 29.84 | 52.69 | 47.27
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1443 | 39.12 | 44.55 | 44.55
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 920 | 63.93 | 70.13 | 69.55
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 899 | 60.96 | 75.44 | 72.26
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 687 | 50.56 | 167.83 | 94.84
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 543 | 120.54 | 141.43 | 117.52
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 141 | 412.94 | 468.89 | 450.89


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3662%2C2979%2C2857%2C2856%2C2771%2C1634%2C1403%2C1391%2C1246%2C1122%2C943%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3662 | 15.45 | 20.11 | 17.63
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2979 | 17.61 | 25.04 | 23.63
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2857 | 21.27 | 22.90 | 22.38
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 2856 | 18.10 | 25.65 | 24.11
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2771 | 20.09 | 24.00 | 24.30
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1634 | 32.71 | 45.95 | 39.66
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1403 | 38.50 | 54.06 | 45.87
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1391 | 41.74 | 49.48 | 47.31
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1246 | 45.25 | 59.69 | 51.63
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1122 | 49.89 | 69.58 | 57.75
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 943 | 53.43 | 99.42 | 71.18


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22fastapi-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3955%2C3647%2C3404%2C3272%2C2982%2C1649%2C1640%2C1598%2C1483%2C1477%2C818%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3955 | 13.70 | 18.36 | 16.84
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3647 | 14.14 | 19.56 | 18.77
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3404 | 14.18 | 20.77 | 20.26
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3272 | 18.44 | 19.90 | 19.77
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2982 | 18.63 | 22.88 | 22.35
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1649 | 29.86 | 44.30 | 42.18
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1640 | 31.07 | 46.17 | 40.14
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1598 | 35.53 | 44.24 | 40.18
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1483 | 38.10 | 48.06 | 43.81
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1477 | 33.87 | 53.03 | 44.65
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 818 | 71.61 | 100.15 | 78.63


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22squall-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2862%2C1610%2C1349%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2862 | 19.66 | 24.96 | 22.46
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1610 | 32.38 | 46.47 | 42.16
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1349 | 44.28 | 60.38 | 47.84


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B270%2C124%2C88%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 270 | 207.22 | 283.42 | 235.81
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 124 | 471.09 | 493.23 | 509.31
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 88 | 640.01 | 782.38 | 697.75


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1322%2C1047%2C976%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1322 | 43.15 | 55.81 | 48.71
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1047 | 50.91 | 74.30 | 61.32
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 976 | 56.26 | 73.49 | 66.70


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3108%2C1678%2C921%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3108 | 18.34 | 23.05 | 20.66
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1678 | 32.38 | 44.91 | 38.45
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 921 | 61.27 | 79.62 | 69.78


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)