# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-20
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
* [The Results](#the-results-2021-12-20)
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

## The Results (2021-12-20)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5102%2C5091%2C5084%2C5039%2C4684%2C4462%2C4323%2C3512%2C2791%2C2117%2C2003%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5102 | 12.72 | 13.73 | 12.72
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 5091 | 12.66 | 13.70 | 12.88
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 5084 | 12.74 | 13.90 | 12.65
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5039 | 13.00 | 14.06 | 12.75
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4684 | 13.81 | 15.08 | 13.68
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4462 | 14.47 | 15.87 | 14.54
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4323 | 15.08 | 16.33 | 14.82
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3512 | 17.48 | 19.53 | 18.31
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2791 | 22.59 | 25.45 | 22.96
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2117 | 29.83 | 30.20 | 30.21
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2003 | 30.87 | 32.79 | 31.92


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3545%2C2547%2C2045%2C1985%2C1840%2C1614%2C1597%2C1579%2C1213%2C1048%2C216%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 3545 | 17.25 | 20.31 | 18.08
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 2547 | 23.01 | 29.03 | 25.07
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2045 | 28.60 | 36.56 | 31.24
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 1985 | 29.73 | 36.67 | 32.19
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1840 | 32.26 | 40.87 | 34.73
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1614 | 37.47 | 46.08 | 39.56
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1597 | 38.47 | 46.60 | 40.00
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1579 | 38.47 | 47.08 | 40.45
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1213 | 52.53 | 52.90 | 52.69
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1048 | 61.95 | 65.87 | 60.97
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 216 | 286.87 | 346.93 | 293.22


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4728%2C4503%2C4450%2C4161%2C3575%2C3505%2C3448%2C3091%2C1807%2C1751%2C1569%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4728 | 13.82 | 14.86 | 13.64
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4503 | 14.62 | 15.76 | 14.19
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 4450 | 14.58 | 15.80 | 14.40
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4161 | 15.67 | 16.87 | 15.49
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3575 | 17.25 | 18.89 | 18.27
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3505 | 18.14 | 19.71 | 18.21
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3448 | 18.50 | 19.15 | 18.53
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3091 | 19.51 | 22.95 | 20.85
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1807 | 35.04 | 35.56 | 35.37
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1751 | 34.90 | 38.76 | 36.48
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1569 | 39.89 | 45.84 | 40.72


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5037%2C4843%2C4826%2C4802%2C4022%2C3945%2C3874%2C3288%2C2327%2C2315%2C1988%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5037 | 12.92 | 13.98 | 12.70
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.2` | 4843 | 13.39 | 14.44 | 13.24
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4826 | 13.45 | 14.48 | 13.37
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4802 | 13.40 | 14.48 | 13.44
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4022 | 15.87 | 16.42 | 15.88
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3945 | 15.99 | 17.42 | 16.22
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3874 | 15.99 | 17.55 | 16.91
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3288 | 18.30 | 21.23 | 19.64
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2327 | 26.43 | 30.86 | 27.47
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2315 | 27.12 | 27.58 | 27.62
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1988 | 30.42 | 33.87 | 32.13


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4822%2C3473%2C2431%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4822 | 13.49 | 14.57 | 13.37
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3473 | 18.20 | 19.70 | 18.41
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2431 | 26.25 | 28.81 | 26.27


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B785%2C186%2C139%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 785 | 77.26 | 94.90 | 81.32
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 186 | 349.84 | 390.63 | 341.00
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 139 | 454.75 | 530.32 | 453.94


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2934%2C1584%2C1144%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 2934 | 20.57 | 24.61 | 21.77
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1584 | 40.92 | 43.62 | 40.34
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1144 | 55.19 | 61.95 | 55.80


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4693%2C3734%2C2203%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4693 | 13.93 | 14.93 | 13.73
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3734 | 16.92 | 18.34 | 17.14
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2203 | 27.79 | 32.43 | 29.01


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)