# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-01-24
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
* [The Results](#the-results-2022-01-24)
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

## The Results (2022-01-24)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5479%2C5397%2C5319%2C5214%2C4955%2C4782%2C4618%2C3876%2C2887%2C2481%2C2109%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5479 | 12.69 | 13.15 | 11.69
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5397 | 12.91 | 13.32 | 11.93
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5319 | 12.96 | 13.43 | 12.11
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5214 | 13.40 | 13.92 | 12.28
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4955 | 14.16 | 14.63 | 12.88
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 4782 | 14.28 | 14.78 | 13.46
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4618 | 15.16 | 15.73 | 13.84
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3876 | 16.87 | 18.05 | 16.54
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 2887 | 22.41 | 25.00 | 22.15
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2481 | 25.52 | 25.82 | 25.78
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2109 | 30.58 | 31.94 | 30.32


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3576%2C2744%2C2299%2C2179%2C1976%2C1850%2C1793%2C1727%2C1357%2C1159%2C219%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3576 | 16.11 | 20.67 | 17.87
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2744 | 21.36 | 27.31 | 23.27
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 2299 | 25.16 | 32.95 | 27.79
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2179 | 26.45 | 34.73 | 29.31
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1976 | 29.74 | 38.99 | 32.39
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1850 | 31.46 | 41.41 | 34.53
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1793 | 32.91 | 42.64 | 35.62
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1727 | 33.79 | 44.94 | 37.11
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1357 | 46.99 | 47.33 | 47.11
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1159 | 52.64 | 60.67 | 55.14
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 219 | 269.06 | 347.90 | 288.08


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4794%2C4749%2C4689%2C4466%2C4059%2C3791%2C3714%2C3460%2C2152%2C1943%2C1698%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4794 | 14.38 | 14.86 | 13.37
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4749 | 14.57 | 15.13 | 13.45
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4689 | 14.91 | 15.44 | 13.61
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4466 | 15.57 | 16.12 | 14.32
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 4059 | 16.51 | 17.36 | 15.93
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3791 | 17.37 | 17.76 | 16.86
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3714 | 18.18 | 18.99 | 17.20
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3460 | 18.42 | 20.14 | 18.51
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2152 | 29.52 | 29.94 | 29.71
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1943 | 32.29 | 35.57 | 32.88
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 1698 | 37.95 | 42.38 | 37.63


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5281%2C5247%2C5124%2C4910%2C4437%2C4290%2C4277%2C3714%2C2677%2C2529%2C2241%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5281 | 13.16 | 13.58 | 12.08
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5247 | 13.23 | 13.60 | 12.18
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5124 | 13.39 | 13.90 | 12.51
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4910 | 13.96 | 14.44 | 13.05
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4437 | 14.79 | 15.14 | 14.40
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4290 | 15.99 | 16.61 | 14.89
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.1` | 4277 | 15.60 | 16.38 | 15.14
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3714 | 17.30 | 18.57 | 17.27
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2677 | 23.64 | 24.18 | 23.89
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.72.0` | 2529 | 25.22 | 28.64 | 25.26
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2241 | 28.43 | 29.77 | 28.52


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5107%2C3579%2C2577%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5107 | 13.64 | 14.13 | 12.56
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3579 | 18.49 | 19.78 | 17.85
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 2577 | 25.27 | 28.21 | 24.79


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1442%2C182%2C137%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1442 | 39.99 | 53.42 | 44.31
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 182 | 341.45 | 414.42 | 349.59
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 137 | 423.61 | 551.47 | 459.22


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4115%2C1741%2C1278%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4115 | 16.83 | 17.45 | 15.53
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1741 | 38.92 | 41.58 | 36.68
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 1278 | 51.12 | 56.89 | 49.97


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4934%2C4065%2C2434%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4934 | 14.05 | 14.50 | 12.96
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 4065 | 16.84 | 17.39 | 15.73
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.72.0` | 2434 | 26.32 | 29.86 | 26.25


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)