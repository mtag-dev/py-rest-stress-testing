# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-01-25
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
* [The Results](#the-results-2022-01-25)
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

## The Results (2022-01-25)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3060%2C2978%2C2869%2C2860%2C2741%2C2505%2C2402%2C1994%2C1737%2C1472%2C1234%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 3060 | 19.58 | 23.43 | 20.93
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2978 | 20.29 | 24.36 | 21.47
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2869 | 20.94 | 25.59 | 22.30
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2860 | 20.72 | 25.69 | 22.38
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2741 | 22.14 | 26.60 | 23.32
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 2505 | 24.07 | 29.36 | 25.51
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2402 | 25.58 | 30.84 | 26.60
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1994 | 31.15 | 36.91 | 32.05
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 1737 | 35.91 | 41.54 | 36.78
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1472 | 42.13 | 44.64 | 43.43
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1234 | 50.77 | 55.77 | 51.80


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2024%2C1627%2C1388%2C1314%2C1252%2C1171%2C1133%2C1072%2C870%2C743%2C171%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2024 | 29.86 | 36.20 | 31.52
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 1627 | 37.85 | 45.37 | 39.25
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 1388 | 44.33 | 53.10 | 46.05
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1314 | 47.05 | 55.83 | 48.59
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1252 | 48.04 | 59.50 | 50.98
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1171 | 51.84 | 63.90 | 54.54
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1133 | 53.54 | 65.84 | 56.39
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1072 | 57.15 | 68.89 | 59.51
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 870 | 72.24 | 75.61 | 73.46
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 743 | 85.37 | 93.45 | 85.96
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 171 | 360.99 | 438.82 | 370.41


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2467%2C2384%2C2371%2C2332%2C2267%2C2095%2C1994%2C1842%2C1198%2C1162%2C1022%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2467 | 24.68 | 30.07 | 25.91
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2384 | 25.30 | 31.03 | 26.79
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2371 | 25.84 | 31.21 | 26.94
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 2332 | 25.99 | 32.07 | 27.39
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2267 | 27.91 | 29.39 | 28.17
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 2095 | 29.06 | 34.93 | 30.53
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1994 | 31.11 | 36.67 | 32.01
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1842 | 33.31 | 39.59 | 34.77
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1198 | 51.60 | 55.98 | 53.39
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1162 | 53.67 | 59.83 | 55.02
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 1022 | 60.90 | 71.22 | 62.49


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2754%2C2680%2C2626%2C2596%2C2576%2C2192%2C2172%2C1978%2C1485%2C1427%2C1278%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2754 | 21.53 | 26.93 | 23.22
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2680 | 22.24 | 27.95 | 23.84
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 2626 | 22.84 | 28.38 | 24.34
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 2596 | 24.08 | 25.51 | 24.61
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2576 | 23.46 | 28.95 | 24.81
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 2192 | 27.84 | 33.92 | 29.15
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 2172 | 28.02 | 34.18 | 29.49
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1978 | 30.93 | 37.22 | 32.29
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1485 | 42.08 | 44.39 | 43.02
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 1427 | 43.16 | 51.98 | 44.74
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1278 | 48.80 | 54.20 | 49.98


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2698%2C2127%2C1488%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2698 | 22.41 | 27.06 | 23.69
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 2127 | 29.74 | 33.89 | 30.04
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 1488 | 41.22 | 48.99 | 42.94


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B939%2C141%2C108%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 939 | 64.11 | 79.63 | 68.02
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 141 | 435.16 | 516.30 | 445.62
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 108 | 543.25 | 700.69 | 585.25


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2202%2C1026%2C784%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2202 | 27.95 | 33.31 | 29.02
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1026 | 61.96 | 70.92 | 62.25
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 784 | 81.81 | 93.58 | 81.37


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2631%2C2045%2C1430%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2631 | 22.61 | 28.17 | 24.27
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 2045 | 30.33 | 36.15 | 31.22
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 1430 | 43.40 | 51.28 | 44.68


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)