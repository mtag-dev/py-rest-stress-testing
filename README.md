# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-09
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
* [The Results](#the-results-2021-11-09)
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * TODO: [PATCH: Update issue](#update-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * TODO: [PATCH: Update issue](#update-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * TODO: [POST: Create issue](#create-pydantic)
    * TODO: [PATCH: Update issue](#update-pydantic)
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

## The Results (2021-11-09)

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4424%2C4236%2C4202%2C4018%2C3994%2C3907%2C3466%2C3346%2C2738%2C1867%2C1811%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4424 | 6.70 | 7.78 | 7.29
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4236 | 6.95 | 8.26 | 7.64
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4202 | 6.99 | 8.11 | 7.70
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4018 | 7.33 | 8.10 | 8.10
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3994 | 7.44 | 8.40 | 8.03
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3907 | 7.58 | 8.94 | 8.21
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3466 | 8.40 | 9.78 | 9.38
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3346 | 8.65 | 10.70 | 9.77
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2738 | 10.65 | 13.33 | 11.78
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1867 | 16.34 | 18.17 | 17.25
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1811 | 17.55 | 18.01 | 17.69


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3426%2C3098%2C2769%2C1931%2C1858%2C1791%2C1770%2C1761%2C1162%2C1154%2C198%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 3426 | 8.70 | 9.62 | 9.37
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3098 | 9.57 | 10.32 | 10.45
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2769 | 10.77 | 11.91 | 11.62
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1931 | 15.16 | 17.55 | 16.62
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1858 | 15.39 | 18.07 | 17.68
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1791 | 16.39 | 18.14 | 17.90
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1770 | 16.69 | 18.95 | 18.18
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1761 | 16.71 | 18.35 | 18.20
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1162 | 26.40 | 27.43 | 27.61
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1154 | 26.29 | 29.14 | 27.74
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 198 | 151.48 | 162.39 | 161.67


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4116%2C4089%2C3852%2C3804%2C3684%2C3379%2C3361%2C3285%2C1813%2C1760%2C1686%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4116 | 7.20 | 8.46 | 7.82
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4089 | 7.20 | 8.62 | 7.91
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 3852 | 7.64 | 9.12 | 8.43
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3804 | 7.75 | 8.81 | 8.53
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3684 | 8.07 | 9.45 | 8.70
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3379 | 8.68 | 10.01 | 9.57
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 3361 | 8.65 | 10.62 | 9.63
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3285 | 8.83 | 10.84 | 9.89
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1813 | 17.14 | 18.62 | 17.70
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1760 | 16.37 | 20.38 | 18.19
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1686 | 18.85 | 19.37 | 18.98


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3213%2C3105%2C2413%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3213 | 9.13 | 10.71 | 10.00
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 3105 | 9.36 | 11.32 | 10.35
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2413 | 12.10 | 15.09 | 13.32


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B345%2C171%2C130%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 345 | 89.43 | 92.22 | 92.56
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 171 | 173.05 | 194.61 | 187.08
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 130 | 226.29 | 245.18 | 246.13


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1719%2C1546%2C1187%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1719 | 16.98 | 20.68 | 18.64
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1546 | 18.73 | 23.68 | 20.74
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1187 | 24.65 | 30.96 | 26.99


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3157%2C3067%2C2056%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 3157 | 9.20 | 11.55 | 10.26
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3067 | 9.47 | 11.50 | 10.50
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 2056 | 14.34 | 16.12 | 15.58


</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B323%2C188%2C85%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 323 | 94.64 | 99.07 | 99.10
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `1.2.0` | 188 | 159.10 | 168.62 | 169.42
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `0.70.0` | 85 | 355.85 | 372.80 | 373.16


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)