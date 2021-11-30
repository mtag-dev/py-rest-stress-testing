# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-30
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
* [The Results](#the-results-2021-11-30)
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

## The Results (2021-11-30)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22squall-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4780%2C4671%2C4584%2C4175%2C4034%2C3878%2C3431%2C2684%2C2496%2C2278%2C1751%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4780 | 12.10 | 15.59 | 13.40
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 4671 | 12.28 | 15.68 | 14.01
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4584 | 12.55 | 15.65 | 13.99
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 4175 | 13.86 | 15.04 | 15.38
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 4034 | 13.91 | 17.80 | 16.11
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3878 | 14.87 | 18.95 | 16.52
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3431 | 16.91 | 21.08 | 18.68
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2684 | 22.02 | 28.09 | 23.97
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2496 | 23.46 | 29.07 | 25.71
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2278 | 25.71 | 27.38 | 28.19
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1751 | 34.79 | 39.74 | 36.55


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22sanic-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2348%2C2074%2C1864%2C1825%2C1811%2C1743%2C1661%2C1576%2C1272%2C1080%2C164%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 2348 | 25.11 | 28.49 | 27.31
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 2074 | 28.67 | 31.70 | 30.80
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 1864 | 32.15 | 35.39 | 34.30
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 1825 | 33.00 | 40.66 | 35.09
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 1811 | 33.02 | 36.49 | 35.34
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 1743 | 33.62 | 38.06 | 36.71
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 1661 | 34.81 | 39.96 | 38.61
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 1576 | 38.28 | 42.08 | 40.61
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 1272 | 47.03 | 50.05 | 50.54
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1080 | 55.42 | 61.41 | 59.13
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 164 | 376.17 | 379.79 | 385.11


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22squall-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4083%2C4005%2C3684%2C3279%2C3087%2C3031%2C3001%2C2396%2C2112%2C1673%2C1385%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4083 | 14.39 | 18.02 | 15.67
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4005 | 14.52 | 18.32 | 15.97
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3684 | 15.37 | 19.73 | 17.66
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3279 | 17.79 | 21.49 | 19.71
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3087 | 19.15 | 23.55 | 20.73
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3031 | 19.97 | 21.58 | 21.20
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3001 | 19.69 | 23.96 | 21.36
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2396 | 24.88 | 31.50 | 26.70
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2112 | 29.30 | 30.38 | 30.34
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1673 | 37.03 | 41.52 | 38.20
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 1385 | 41.69 | 54.26 | 46.17


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22squall-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4382%2C4288%2C3980%2C3465%2C3435%2C3427%2C3191%2C2367%2C2333%2C2173%2C1857%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon-raw/) `3.0.1` | 4382 | 13.00 | 16.46 | 14.62
| [muffin-raw](https://pypi.org/project/muffin-raw/) `0.86.0` | 4288 | 13.38 | 17.03 | 14.91
| [blacksheep-raw](https://pypi.org/project/blacksheep-raw/) `1.2.0` | 3980 | 14.03 | 18.20 | 16.25
| [emmett-raw](https://pypi.org/project/emmett-raw/) `2.3.2` | 3465 | 16.47 | 20.53 | 18.69
| [starlette-raw](https://pypi.org/project/starlette-raw/) `0.16.0` | 3435 | 17.14 | 20.84 | 18.61
| [baize-raw](https://pypi.org/project/baize-raw/) `0.12.1` | 3427 | 17.70 | 19.01 | 18.94
| [sanic-raw](https://pypi.org/project/sanic-raw/) `21.9.1` | 3191 | 18.27 | 22.18 | 20.14
| [squall-raw](https://pypi.org/project/squall-raw/) `` | 2367 | 25.42 | 32.25 | 27.03
| [aiohttp-raw](https://pypi.org/project/aiohttp-raw/) `3.8.0` | 2333 | 26.70 | 27.70 | 27.46
| [fastapi-raw](https://pypi.org/project/fastapi-raw/) `0.70.0` | 2173 | 26.64 | 33.74 | 29.44
| [quart-raw](https://pypi.org/project/quart-raw/) `0.15.1` | 1857 | 33.22 | 37.29 | 34.42


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22squall-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3067%2C2205%2C2156%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3067 | 18.75 | 23.42 | 20.85
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2205 | 26.97 | 33.37 | 29.00
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2156 | 26.71 | 34.28 | 29.66


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B330%2C134%2C107%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 330 | 172.70 | 188.48 | 195.18
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 134 | 448.30 | 461.12 | 469.19
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 107 | 581.04 | 592.19 | 592.99


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1552%2C1459%2C1065%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 1552 | 39.21 | 47.49 | 41.22
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 1459 | 39.60 | 49.19 | 43.79
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 1065 | 55.33 | 69.46 | 59.97


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%2C%22squall-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3421%2C2165%2C2123%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep-dataclasses/) `1.2.0` | 3421 | 17.14 | 20.89 | 18.71
| [fastapi-dataclasses](https://pypi.org/project/fastapi-dataclasses/) `0.70.0` | 2165 | 26.63 | 33.40 | 29.56
| [squall-dataclasses](https://pypi.org/project/squall-dataclasses/) `` | 2123 | 28.39 | 34.92 | 30.14


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)