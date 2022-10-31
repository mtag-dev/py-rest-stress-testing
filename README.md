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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5274%2C5269%2C5214%2C5116%2C4699%2C4641%2C4484%2C3325%2C2778%2C2202%2C2135%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 5274 | 12.37 | 13.30 | 12.21
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5269 | 12.10 | 13.16 | 12.33
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 5214 | 12.35 | 13.33 | 12.43
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 5116 | 12.76 | 13.67 | 12.58
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 4699 | 13.75 | 14.83 | 13.63
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 4641 | 13.55 | 14.73 | 14.06
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 4484 | 14.45 | 15.60 | 14.28
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3325 | 18.28 | 21.04 | 19.43
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2778 | 22.19 | 25.63 | 23.07
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 2202 | 28.67 | 28.93 | 29.03
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2135 | 28.33 | 30.98 | 29.95


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3660%2C2595%2C2315%2C1940%2C1897%2C1720%2C1650%2C1597%2C1257%2C1126%2C208%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3660 | 15.50 | 20.12 | 17.50
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2595 | 22.12 | 28.79 | 24.62
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 2315 | 25.00 | 32.02 | 27.61
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 1940 | 29.80 | 37.99 | 32.98
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 1897 | 30.63 | 40.36 | 33.67
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 1720 | 34.14 | 44.12 | 37.13
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 1650 | 36.02 | 45.73 | 38.72
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 1597 | 36.91 | 47.49 | 40.00
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1257 | 50.70 | 51.13 | 50.82
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1126 | 56.20 | 61.44 | 56.73
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 208 | 304.65 | 349.30 | 304.33


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4717%2C4615%2C4553%2C4279%2C3845%2C3612%2C3527%2C2982%2C1926%2C1742%2C1574%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4717 | 13.58 | 14.67 | 13.70
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 4615 | 14.35 | 15.32 | 13.93
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 4553 | 14.31 | 15.40 | 14.05
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 4279 | 15.14 | 16.18 | 15.01
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3845 | 16.11 | 17.58 | 17.07
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 3612 | 17.55 | 18.96 | 17.67
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 3527 | 18.09 | 18.62 | 18.12
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 2982 | 20.24 | 24.12 | 21.54
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1926 | 31.41 | 35.33 | 33.19
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1742 | 36.41 | 36.76 | 36.70
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 1574 | 40.05 | 45.21 | 40.57


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5123%2C5049%2C4964%2C4810%2C4118%2C4083%2C3962%2C3205%2C2403%2C2154%2C2143%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 5123 | 12.62 | 13.56 | 12.51
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 5049 | 12.94 | 13.75 | 12.73
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 4964 | 12.98 | 13.87 | 13.03
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4810 | 13.22 | 14.27 | 13.44
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 4118 | 15.47 | 15.93 | 15.51
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 4083 | 15.35 | 16.62 | 15.69
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.10` | 3962 | 15.58 | 16.94 | 16.65
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3205 | 18.96 | 21.80 | 20.09
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.73.0` | 2403 | 25.73 | 29.86 | 26.63
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2154 | 27.88 | 30.30 | 29.65
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 2143 | 29.47 | 30.02 | 29.88


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5043%2C3137%2C2120%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5043 | 12.78 | 13.82 | 12.82
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 3137 | 19.88 | 22.12 | 20.44
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2120 | 29.77 | 32.86 | 30.13


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1420%2C153%2C84%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1420 | 42.16 | 52.60 | 44.98
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 153 | 406.07 | 481.31 | 411.69
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 84 | 687.34 | 901.04 | 745.21


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3978%2C1327%2C914%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 3978 | 15.98 | 17.23 | 16.11
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 1327 | 48.11 | 53.51 | 48.14
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 914 | 71.18 | 76.63 | 69.85


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4807%2C3729%2C2473%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4807 | 13.30 | 14.41 | 13.39
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 3729 | 16.82 | 18.08 | 17.19
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.73.0` | 2473 | 24.90 | 29.26 | 25.84


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)