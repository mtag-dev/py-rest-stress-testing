# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-25
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
* [The Results](#the-results-2021-11-25)
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

## The Results (2021-11-25)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22muffin-raw%22%2C%22aiohttp-raw%22%2C%22starlette-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4766%2C4650%2C4311%2C4092%2C3569%2C3415%2C2641%2C2518%2C2439%2C1918%2C1573%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4766 | 6.40 | 7.17 | 6.76
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4650 | 6.62 | 7.32 | 6.88
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4311 | 6.90 | 8.10 | 7.53
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4092 | 7.29 | 8.82 | 7.95
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3569 | 8.50 | 10.16 | 9.09
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3415 | 8.81 | 10.64 | 9.42
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2641 | 9.15 | 16.68 | 12.84
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2518 | 12.55 | 12.82 | 12.77
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2439 | 10.33 | 19.31 | 22.52
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1918 | 13.37 | 21.44 | 18.18
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1573 | 17.93 | 19.54 | 21.12


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22emmett-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3187%2C2604%2C1944%2C1921%2C1844%2C1759%2C1742%2C1519%2C1379%2C695%2C168%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3187 | 9.21 | 9.93 | 10.09
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2604 | 11.27 | 12.23 | 12.32
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1944 | 14.81 | 18.19 | 16.44
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 1921 | 11.86 | 26.19 | 18.72
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1844 | 15.59 | 18.55 | 17.35
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1759 | 16.52 | 19.42 | 18.17
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1742 | 16.66 | 19.85 | 18.42
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1519 | 18.88 | 21.01 | 21.20
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1379 | 23.05 | 23.59 | 23.20
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 695 | 34.10 | 58.71 | 50.36
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 168 | 181.16 | 184.94 | 190.33


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4078%2C4076%2C4001%2C3712%2C3415%2C3070%2C3017%2C2523%2C2191%2C1643%2C1070%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4078 | 7.44 | 8.83 | 7.87
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4076 | 7.47 | 9.14 | 7.84
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4001 | 7.77 | 9.18 | 7.98
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3712 | 7.85 | 9.46 | 8.75
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3415 | 8.94 | 10.72 | 9.42
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3070 | 9.78 | 11.98 | 10.52
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3017 | 10.47 | 10.88 | 10.58
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2523 | 10.59 | 13.25 | 15.00
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2191 | 14.42 | 14.76 | 14.60
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1643 | 19.17 | 19.95 | 19.51
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1070 | 25.72 | 36.29 | 30.85


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22baize-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22muffin-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4883%2C4390%2C3758%2C3429%2C3365%2C3269%2C3047%2C2380%2C2368%2C1845%2C1822%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4883 | 6.32 | 7.50 | 6.58
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4390 | 7.07 | 8.27 | 7.28
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3758 | 8.13 | 9.04 | 8.64
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3429 | 8.97 | 10.59 | 9.33
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3365 | 8.93 | 10.63 | 9.65
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3269 | 9.43 | 11.12 | 9.85
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3047 | 9.13 | 10.04 | 11.82
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2380 | 13.16 | 13.86 | 13.45
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2368 | 13.41 | 13.83 | 13.50
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1845 | 17.00 | 17.55 | 17.34
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 1822 | 15.66 | 25.58 | 18.50


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3057%2C2791%2C1908%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3057 | 10.03 | 11.89 | 10.53
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 2791 | 10.54 | 13.08 | 11.68
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1908 | 13.94 | 17.55 | 18.33


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B293%2C96%2C96%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 293 | 101.98 | 105.21 | 108.77
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 96 | 309.25 | 403.53 | 334.33
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 96 | 289.68 | 357.91 | 329.06


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1709%2C1480%2C966%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1709 | 17.93 | 21.18 | 18.70
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1480 | 21.30 | 23.72 | 21.59
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 966 | 29.67 | 36.53 | 34.01


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3596%2C2592%2C2334%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3596 | 8.70 | 9.93 | 8.91
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2592 | 12.01 | 13.55 | 12.35
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2334 | 13.34 | 13.98 | 13.69


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2817%2C2213%2C1633%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 2817 | 10.27 | 12.44 | 11.63
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2213 | 11.64 | 17.08 | 16.05
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1633 | 15.80 | 21.19 | 20.62


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B244%2C138%2C55%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 244 | 116.40 | 123.97 | 136.83
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 138 | 201.62 | 266.71 | 230.62
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 55 | 479.23 | 578.85 | 564.88


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1631%2C1530%2C834%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 1631 | 18.62 | 22.52 | 19.59
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1530 | 20.66 | 23.30 | 20.88
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 834 | 36.35 | 40.80 | 38.74


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3614%2C2556%2C1643%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3614 | 8.58 | 9.91 | 8.86
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2556 | 12.23 | 13.92 | 12.54
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 1643 | 16.36 | 23.93 | 20.19


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)