# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-29
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
* [The Results](#the-results-2021-11-29)
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

## The Results (2021-11-29)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22fastapi-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4342%2C4312%2C4276%2C4100%2C3991%2C3691%2C3410%2C2819%2C2797%2C1846%2C1808%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4342 | 6.81 | 8.32 | 7.41
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4312 | 6.76 | 8.21 | 7.54
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4276 | 6.83 | 8.27 | 7.57
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4100 | 7.22 | 8.06 | 7.93
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3991 | 7.32 | 9.00 | 8.18
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3691 | 8.02 | 9.62 | 8.72
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3410 | 8.10 | 10.78 | 9.65
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2819 | 10.28 | 13.02 | 11.43
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2797 | 9.97 | 13.22 | 11.81
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1846 | 16.56 | 18.43 | 17.38
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1808 | 17.55 | 18.05 | 17.71


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3375%2C3160%2C2773%2C1938%2C1855%2C1645%2C1638%2C1251%2C1162%2C1077%2C195%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3375 | 8.73 | 9.89 | 9.53
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3160 | 9.47 | 10.11 | 10.19
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2773 | 11.07 | 13.04 | 11.62
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1938 | 15.19 | 16.75 | 16.54
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1855 | 15.75 | 18.01 | 17.38
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1645 | 17.41 | 21.25 | 19.48
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1638 | 17.09 | 20.70 | 19.69
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1251 | 23.38 | 27.71 | 25.72
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1162 | 25.81 | 26.98 | 27.58
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1077 | 27.01 | 31.54 | 29.85
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 195 | 157.74 | 163.29 | 162.52


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3957%2C3910%2C3610%2C3303%2C3042%2C2908%2C2894%2C2087%2C1663%2C1534%2C1289%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3957 | 7.44 | 9.04 | 8.18
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3910 | 7.64 | 8.95 | 8.19
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3610 | 8.16 | 9.37 | 9.05
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3303 | 8.63 | 11.14 | 9.83
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3042 | 10.15 | 11.72 | 10.67
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2908 | 9.70 | 12.76 | 11.34
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 2894 | 10.60 | 11.72 | 11.16
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2087 | 14.08 | 17.18 | 15.51
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1663 | 18.01 | 20.11 | 19.33
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1534 | 19.48 | 20.31 | 21.05
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1289 | 21.82 | 27.82 | 27.05


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4236%2C4102%2C3938%2C3623%2C3321%2C3269%2C2986%2C2817%2C2089%2C1940%2C1854%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4236 | 6.99 | 8.40 | 7.59
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4102 | 7.19 | 8.72 | 7.88
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3938 | 7.35 | 9.27 | 8.24
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3623 | 8.05 | 9.14 | 9.05
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3321 | 9.29 | 10.32 | 9.68
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3269 | 9.29 | 10.87 | 9.90
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 2986 | 9.72 | 12.23 | 10.80
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 2817 | 10.27 | 13.03 | 11.58
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2089 | 13.15 | 17.43 | 15.60
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1940 | 16.07 | 16.75 | 16.56
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1854 | 16.19 | 18.01 | 17.50


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3523%2C3308%2C2471%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3523 | 8.29 | 10.33 | 9.21
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3308 | 8.95 | 10.99 | 9.72
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2471 | 11.85 | 14.91 | 13.01


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B566%2C171%2C132%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 566 | 52.02 | 60.08 | 56.65
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 171 | 173.94 | 190.22 | 186.79
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 132 | 228.01 | 239.90 | 242.19


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2313%2C1475%2C1094%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2313 | 12.38 | 15.63 | 13.88
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1475 | 19.21 | 24.13 | 21.80
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1094 | 25.57 | 33.99 | 29.40


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3902%2C3474%2C1965%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3902 | 7.49 | 9.37 | 8.32
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3474 | 8.45 | 10.45 | 9.26
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1965 | 15.24 | 18.82 | 16.36


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10560%2C3282%2C2091%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10560 | 2.71 | 3.04 | 3.05
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3282 | 8.96 | 10.65 | 9.81
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2091 | 13.74 | 17.50 | 15.33


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B9650%2C189%2C83%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 9650 | 3.02 | 3.48 | 3.33
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 189 | 155.89 | 170.04 | 168.47
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 83 | 349.54 | 383.00 | 378.50


</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B9937%2C1377%2C915%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 9937 | 2.86 | 3.11 | 3.24
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 1377 | 21.54 | 26.36 | 23.35
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 915 | 31.63 | 39.25 | 35.12


</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B10719%2C3466%2C2172%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 10719 | 2.50 | 3.31 | 3.00
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3466 | 8.51 | 10.03 | 9.29
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2172 | 13.38 | 16.66 | 14.85


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)