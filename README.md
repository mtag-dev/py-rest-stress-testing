# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-18
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
* [The Results](#the-results-2021-11-18)
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * [PUT: Update task](#update-task-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * [PUT: Update task](#update-task-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * [POST: Create task](#create-task-pydantic)
    * [PUT: Update task](#update-task-pydantic)
    * [GET: Sprint board](#sprint-pydantic)


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

## The Results (2021-11-18)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22baize-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4801%2C4423%2C4333%2C4182%2C4035%2C3819%2C3789%2C2813%2C2482%2C2295%2C1959%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4801 | 6.31 | 7.50 | 6.71
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4423 | 6.84 | 8.39 | 7.25
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4333 | 6.66 | 8.21 | 7.72
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4182 | 7.14 | 8.65 | 7.71
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 4035 | 7.49 | 8.53 | 7.93
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3819 | 7.92 | 9.36 | 8.46
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3789 | 7.33 | 9.53 | 8.63
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2813 | 9.56 | 12.28 | 13.49
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2482 | 11.88 | 14.64 | 12.98
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2295 | 12.60 | 12.99 | 15.38
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1959 | 15.95 | 16.67 | 16.32


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3185%2C2906%2C2805%2C1817%2C1792%2C1785%2C1758%2C1547%2C1349%2C1004%2C160%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3185 | 8.35 | 11.49 | 10.45
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2906 | 9.75 | 12.06 | 11.17
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2805 | 10.23 | 12.34 | 11.44
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1817 | 15.84 | 18.88 | 17.60
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1792 | 16.00 | 20.28 | 17.92
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1785 | 16.26 | 19.37 | 17.91
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1758 | 16.19 | 20.18 | 18.24
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1547 | 18.19 | 21.94 | 20.85
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1349 | 22.98 | 23.77 | 23.85
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1004 | 27.86 | 32.48 | 35.31
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 160 | 179.89 | 210.79 | 197.67


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22emmett-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4134%2C3937%2C3880%2C3796%2C3793%2C3567%2C3559%2C3220%2C2083%2C1492%2C1421%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4134 | 7.12 | 8.31 | 7.80
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3937 | 7.39 | 9.30 | 8.22
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3880 | 7.44 | 9.13 | 8.43
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3796 | 7.98 | 9.06 | 8.64
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3793 | 7.84 | 9.60 | 8.50
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3567 | 8.72 | 10.23 | 9.01
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3559 | 8.65 | 10.47 | 8.98
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3220 | 9.19 | 10.73 | 10.25
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2083 | 14.01 | 15.06 | 15.72
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1492 | 20.25 | 23.91 | 21.49
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1421 | 18.37 | 23.08 | 25.01


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22baize-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4858%2C4763%2C4507%2C4461%2C4291%2C4273%2C3629%2C3422%2C2916%2C2456%2C1220%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4858 | 5.88 | 7.23 | 6.62
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4763 | 5.76 | 7.34 | 6.89
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4507 | 6.58 | 7.89 | 7.27
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4461 | 6.25 | 8.25 | 7.31
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4291 | 6.36 | 9.30 | 7.64
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 4273 | 7.66 | 8.30 | 7.51
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3629 | 8.62 | 9.90 | 8.85
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3422 | 9.00 | 10.66 | 9.78
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2916 | 10.42 | 12.18 | 11.01
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2456 | 12.49 | 13.15 | 13.18
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1220 | 21.39 | 34.90 | 26.78


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3198%2C3105%2C2145%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3198 | 9.65 | 11.30 | 10.04
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3105 | 9.61 | 11.60 | 10.41
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2145 | 13.92 | 16.38 | 15.02


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B301%2C129%2C103%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 301 | 100.27 | 104.08 | 106.10
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 129 | 224.14 | 258.93 | 246.10
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 103 | 284.63 | 300.63 | 306.49


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1794%2C1413%2C1025%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1794 | 17.37 | 18.72 | 17.82
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1413 | 21.87 | 25.43 | 22.74
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1025 | 29.73 | 34.19 | 31.19


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3394%2C2699%2C2296%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3394 | 8.97 | 10.56 | 9.45
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2699 | 11.68 | 13.02 | 11.87
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2296 | 13.58 | 14.46 | 13.92


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3135%2C2869%2C1873%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3135 | 9.80 | 11.24 | 10.24
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2869 | 10.09 | 12.46 | 11.46
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1873 | 15.91 | 18.84 | 17.16


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B275%2C153%2C66%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 275 | 106.35 | 114.99 | 115.78
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 153 | 188.07 | 208.61 | 207.44
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 66 | 448.59 | 477.62 | 478.02


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1737%2C1382%2C844%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1737 | 17.90 | 19.36 | 18.41
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1382 | 21.63 | 25.84 | 23.35
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 844 | 36.72 | 42.42 | 37.90


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3482%2C2707%2C2078%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3482 | 8.74 | 10.09 | 9.85
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2707 | 11.40 | 13.14 | 11.86
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2078 | 14.45 | 16.57 | 15.71


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)