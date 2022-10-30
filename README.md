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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2883%2C2827%2C2787%2C2685%2C2442%2C2411%2C2231%2C1965%2C1676%2C1430%2C1245%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2883 | 20.60 | 25.12 | 22.22
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2827 | 20.91 | 26.09 | 22.63
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 2787 | 21.48 | 26.16 | 23.03
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2685 | 22.19 | 27.40 | 23.85
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2442 | 24.74 | 30.37 | 26.19
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2411 | 24.52 | 31.03 | 26.58
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2231 | 27.40 | 33.31 | 28.67
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1965 | 30.90 | 37.10 | 32.63
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1676 | 37.13 | 43.91 | 38.14
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1430 | 43.62 | 45.29 | 44.70
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1245 | 49.53 | 55.49 | 51.34


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2148%2C1717%2C1438%2C1222%2C1195%2C1135%2C1124%2C1046%2C847%2C756%2C159%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2148 | 27.65 | 34.12 | 29.75
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 1717 | 34.63 | 42.92 | 37.17
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 1438 | 41.81 | 51.07 | 44.43
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1222 | 48.98 | 60.67 | 52.26
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1195 | 50.38 | 61.08 | 53.48
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1135 | 52.27 | 66.22 | 56.28
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 1124 | 53.41 | 65.74 | 56.76
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1046 | 57.66 | 69.44 | 61.06
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 847 | 74.61 | 77.24 | 75.38
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 756 | 82.10 | 92.80 | 84.48
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 159 | 386.56 | 461.83 | 396.59


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2446%2C2375%2C2349%2C2196%2C2170%2C2074%2C1954%2C1762%2C1259%2C1197%2C976%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2446 | 24.55 | 30.81 | 26.13
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2375 | 25.73 | 31.44 | 26.89
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2349 | 25.95 | 31.73 | 27.21
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 2196 | 27.75 | 33.66 | 29.11
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2170 | 29.10 | 30.77 | 29.45
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2074 | 29.36 | 35.26 | 30.93
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1954 | 31.68 | 37.74 | 32.69
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1762 | 34.30 | 41.60 | 36.36
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1259 | 49.99 | 52.11 | 50.79
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1197 | 52.02 | 57.49 | 53.36
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 976 | 64.22 | 75.05 | 65.91


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2768%2C2683%2C2506%2C2495%2C2399%2C2193%2C2126%2C1842%2C1479%2C1424%2C1262%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2768 | 21.47 | 26.86 | 23.07
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2683 | 22.09 | 28.05 | 23.83
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2506 | 25.05 | 26.56 | 25.50
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.7` | 2495 | 23.93 | 30.28 | 25.64
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2399 | 25.27 | 31.00 | 26.67
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2193 | 27.85 | 34.08 | 29.11
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2126 | 28.46 | 34.77 | 30.17
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1842 | 32.88 | 39.56 | 34.75
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1479 | 41.98 | 44.64 | 43.24
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1424 | 43.98 | 52.10 | 44.85
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1262 | 49.43 | 54.99 | 50.60


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2609%2C1841%2C1250%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2609 | 22.99 | 28.77 | 24.53
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 1841 | 33.80 | 39.00 | 34.72
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 1250 | 50.44 | 58.13 | 51.13


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B974%2C108%2C64%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 974 | 61.54 | 76.13 | 65.52
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 108 | 558.53 | 702.76 | 581.43
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 64 | 945.92 | 1164.48 | 967.88


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2053%2C856%2C619%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2053 | 30.07 | 35.68 | 31.14
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 856 | 75.34 | 85.17 | 74.64
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 619 | 104.52 | 117.33 | 102.93


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2435%2C1967%2C1433%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2435 | 24.86 | 30.69 | 26.24
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.7` | 1967 | 31.56 | 37.28 | 32.50
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 1433 | 42.61 | 51.84 | 44.59


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)