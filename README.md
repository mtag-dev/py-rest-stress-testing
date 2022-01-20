# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-01-20
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
* [The Results](#the-results-2022-01-20)
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

## The Results (2022-01-20)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5505%2C5413%2C5386%2C5284%2C5023%2C4837%2C4631%2C3934%2C2953%2C2533%2C2120%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5505 | 12.68 | 13.09 | 11.62
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5413 | 12.82 | 13.22 | 11.87
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5386 | 12.87 | 13.26 | 11.94
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5284 | 13.21 | 13.59 | 12.11
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 5023 | 14.01 | 14.41 | 12.72
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 4837 | 14.15 | 14.62 | 13.30
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4631 | 15.20 | 15.60 | 13.80
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3934 | 16.74 | 17.77 | 16.27
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 2953 | 22.05 | 24.22 | 21.67
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2533 | 25.06 | 25.37 | 25.25
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2120 | 30.39 | 31.71 | 30.14


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3632%2C2820%2C2330%2C2204%2C1991%2C1884%2C1850%2C1766%2C1384%2C1158%2C222%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3632 | 16.04 | 20.35 | 17.59
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2820 | 20.59 | 26.62 | 22.64
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 2330 | 24.79 | 32.44 | 27.41
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2204 | 25.88 | 34.42 | 28.99
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1991 | 28.94 | 38.65 | 32.09
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1884 | 30.79 | 40.82 | 33.91
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1850 | 31.93 | 41.46 | 34.53
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1766 | 32.91 | 43.29 | 36.17
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1384 | 46.26 | 46.51 | 46.25
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1158 | 52.44 | 60.72 | 55.12
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 222 | 279.78 | 340.24 | 284.46


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4841%2C4826%2C4684%2C4444%2C4134%2C3838%2C3813%2C3468%2C2201%2C1958%2C1743%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4841 | 14.45 | 14.87 | 13.19
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4826 | 14.32 | 14.72 | 13.27
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4684 | 14.95 | 15.46 | 13.63
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4444 | 15.66 | 16.20 | 14.39
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 4134 | 16.30 | 17.05 | 15.59
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3838 | 17.19 | 17.51 | 16.65
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3813 | 18.12 | 18.59 | 16.75
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3468 | 18.34 | 20.08 | 18.45
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2201 | 28.93 | 29.27 | 29.05
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1958 | 32.20 | 34.91 | 32.64
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 1743 | 37.65 | 41.56 | 36.67


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5326%2C5240%2C5160%2C4950%2C4457%2C4331%2C4321%2C3720%2C2696%2C2611%2C2220%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5326 | 13.04 | 13.40 | 11.98
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5240 | 13.18 | 13.54 | 12.23
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5160 | 13.35 | 13.95 | 12.38
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4950 | 13.94 | 14.33 | 12.93
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4457 | 14.71 | 15.05 | 14.33
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 4331 | 15.43 | 16.17 | 14.91
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4321 | 15.94 | 16.38 | 14.78
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3720 | 17.21 | 18.55 | 17.21
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2696 | 23.55 | 23.96 | 23.72
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 2611 | 24.50 | 27.88 | 24.47
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2220 | 28.52 | 30.16 | 28.78


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5126%2C3671%2C2617%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5126 | 13.53 | 13.99 | 12.52
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3671 | 18.28 | 19.20 | 17.39
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 2617 | 25.48 | 27.91 | 24.49


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1439%2C185%2C139%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1439 | 39.72 | 53.45 | 44.42
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 185 | 340.05 | 403.69 | 342.72
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 139 | 446.32 | 541.32 | 452.62


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4154%2C1763%2C1292%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4154 | 16.83 | 17.32 | 15.37
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1763 | 38.16 | 40.68 | 36.22
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 1292 | 50.88 | 56.50 | 49.42


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4965%2C4087%2C2585%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4965 | 13.97 | 14.35 | 12.87
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 4087 | 16.67 | 17.15 | 15.63
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 2585 | 25.00 | 28.24 | 24.71


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)