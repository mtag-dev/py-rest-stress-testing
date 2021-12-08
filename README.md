# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-08
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
* [The Results](#the-results-2021-12-08)
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

## The Results (2021-12-08)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5742%2C5596%2C5422%2C5389%2C4966%2C4888%2C4673%2C4138%2C2972%2C2685%2C2133%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 5742 | 12.09 | 12.53 | 11.23
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 5596 | 12.47 | 12.95 | 11.46
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 5422 | 12.58 | 13.27 | 11.89
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5389 | 12.94 | 13.40 | 11.88
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 4966 | 14.11 | 14.70 | 12.88
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4888 | 13.35 | 14.91 | 13.18
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 4673 | 15.01 | 15.61 | 13.68
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 4138 | 16.28 | 17.33 | 15.49
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2972 | 21.73 | 24.18 | 21.54
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2685 | 23.67 | 24.25 | 23.82
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 2133 | 30.17 | 31.76 | 29.97


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3875%2C2767%2C2295%2C2211%2C2002%2C1845%2C1823%2C1749%2C1461%2C1167%2C216%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 3875 | 14.85 | 19.39 | 16.50
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2767 | 20.71 | 27.58 | 23.08
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2295 | 25.05 | 33.67 | 27.84
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2211 | 25.95 | 34.56 | 28.92
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2002 | 28.68 | 38.93 | 31.94
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 1845 | 31.55 | 41.66 | 34.64
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1823 | 31.41 | 42.65 | 35.06
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 1749 | 33.05 | 43.84 | 36.52
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1461 | 43.60 | 44.16 | 43.77
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1167 | 51.51 | 60.78 | 54.76
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 216 | 287.83 | 347.87 | 293.85


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5107%2C4859%2C4754%2C4542%2C4133%2C3794%2C3778%2C3518%2C2283%2C1958%2C1712%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 5107 | 13.59 | 14.07 | 12.57
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4859 | 14.39 | 14.95 | 13.15
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4754 | 14.69 | 15.32 | 13.43
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 4542 | 15.35 | 15.93 | 14.09
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4133 | 16.09 | 17.45 | 15.62
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 3794 | 17.33 | 17.74 | 16.85
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3778 | 17.93 | 18.72 | 16.91
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3518 | 18.04 | 19.99 | 18.22
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2283 | 27.98 | 28.46 | 28.01
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1958 | 32.07 | 35.22 | 32.65
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1712 | 37.62 | 42.79 | 37.32


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5402%2C5270%2C5248%2C5178%2C4437%2C4373%2C4361%2C3835%2C2709%2C2610%2C2244%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5402 | 12.83 | 13.27 | 11.82
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 5270 | 13.07 | 13.57 | 12.17
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 5248 | 13.18 | 13.64 | 12.23
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 5178 | 13.24 | 14.07 | 12.35
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 4437 | 14.76 | 15.14 | 14.40
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4373 | 15.41 | 16.34 | 14.83
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 4361 | 15.71 | 16.34 | 14.65
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 3835 | 16.76 | 18.32 | 16.74
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2709 | 23.45 | 23.85 | 23.61
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2610 | 24.64 | 27.87 | 24.48
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 2244 | 28.31 | 29.69 | 28.48


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5237%2C3640%2C2620%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 5237 | 13.34 | 13.80 | 12.24
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 3640 | 18.14 | 19.58 | 17.55
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2620 | 24.82 | 27.79 | 24.40


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B813%2C181%2C137%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 813 | 70.83 | 95.34 | 78.53
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 181 | 344.76 | 423.24 | 351.00
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 137 | 446.57 | 542.72 | 461.04


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3214%2C1726%2C1299%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 3214 | 19.86 | 22.51 | 19.88
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 1726 | 38.55 | 41.53 | 37.01
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1299 | 50.11 | 56.06 | 49.17


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5120%2C4087%2C2545%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 5120 | 13.59 | 14.02 | 12.51
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 4087 | 16.57 | 17.26 | 15.65
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 2545 | 25.18 | 28.80 | 25.10


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)