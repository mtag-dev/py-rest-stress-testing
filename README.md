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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4829%2C4367%2C4191%2C4070%2C4011%2C3821%2C3489%2C2839%2C2436%2C1995%2C1539%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4829 | 12.98 | 14.36 | 13.56
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4367 | 13.96 | 16.01 | 14.89
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4191 | 14.07 | 16.77 | 15.79
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4070 | 14.77 | 17.43 | 16.01
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 4011 | 14.95 | 17.09 | 16.59
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3821 | 16.00 | 18.35 | 16.92
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3489 | 17.24 | 20.41 | 18.45
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2839 | 20.56 | 25.96 | 22.94
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2436 | 24.56 | 30.32 | 26.46
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1995 | 30.23 | 33.18 | 32.05
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1539 | 39.21 | 45.31 | 41.64


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3015%2C2172%2C1884%2C1743%2C1598%2C1545%2C1355%2C1318%2C1093%2C929%2C206%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3015 | 19.80 | 23.77 | 21.39
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2172 | 27.73 | 33.53 | 29.44
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 1884 | 32.06 | 38.48 | 34.13
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 1743 | 34.18 | 42.16 | 36.80
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1598 | 37.97 | 45.73 | 40.01
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1545 | 40.12 | 47.43 | 41.36
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1355 | 44.79 | 54.70 | 47.22
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 1318 | 46.51 | 55.48 | 48.47
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1093 | 55.84 | 59.92 | 58.57
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 929 | 66.36 | 75.84 | 68.78
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 206 | 312.41 | 348.75 | 306.60


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4314%2C4216%2C3708%2C3565%2C3156%2C3124%2C3012%2C2739%2C1761%2C1581%2C1415%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4314 | 14.39 | 16.02 | 15.11
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4216 | 14.58 | 16.82 | 15.37
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3708 | 16.49 | 19.00 | 17.36
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 3565 | 16.44 | 19.92 | 18.33
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 3156 | 17.93 | 22.30 | 21.15
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3124 | 18.79 | 23.34 | 20.56
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3012 | 20.20 | 22.66 | 21.29
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2739 | 21.07 | 26.89 | 23.77
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1761 | 34.82 | 36.59 | 36.35
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1581 | 38.15 | 44.31 | 40.44
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1415 | 43.13 | 50.68 | 45.43


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4462%2C4342%2C4308%2C3973%2C3383%2C3375%2C3206%2C2781%2C2190%2C2177%2C1762%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4462 | 13.37 | 15.52 | 14.76
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4342 | 14.10 | 15.98 | 15.07
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4308 | 13.94 | 16.53 | 15.04
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3973 | 15.34 | 17.62 | 16.32
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3383 | 18.14 | 19.93 | 18.94
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 3375 | 16.70 | 20.32 | 19.91
| [starlette-raw](https://pypi.org/project/starlette/) `0.18.0` | 3206 | 18.56 | 22.26 | 20.16
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2781 | 20.66 | 26.39 | 23.54
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2190 | 27.69 | 32.71 | 29.30
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2177 | 28.29 | 29.57 | 29.39
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1762 | 34.31 | 39.68 | 36.34


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4677%2C3091%2C2111%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4677 | 13.28 | 15.01 | 13.97
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3091 | 18.86 | 23.34 | 20.98
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2111 | 28.82 | 34.00 | 30.51


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1352%2C181%2C129%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1352 | 45.12 | 54.76 | 47.26
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 181 | 348.56 | 403.95 | 351.24
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 129 | 484.20 | 565.66 | 489.61


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3681%2C1402%2C1056%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 3681 | 16.65 | 18.97 | 17.60
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1402 | 44.11 | 51.20 | 45.55
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 1056 | 58.34 | 68.13 | 60.48


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4081%2C3219%2C1931%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4081 | 14.64 | 17.02 | 16.03
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3219 | 18.10 | 21.90 | 20.14
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 1931 | 30.56 | 38.04 | 33.42


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)