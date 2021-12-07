# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-07
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
* [The Results](#the-results-2021-12-07)
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

## The Results (2021-12-07)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4912%2C4065%2C3999%2C3941%2C3485%2C3271%2C2926%2C2845%2C2443%2C2208%2C1560%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4912 | 11.76 | 15.16 | 13.08
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 4065 | 14.06 | 17.57 | 15.89
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3999 | 14.19 | 18.23 | 16.11
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3941 | 14.05 | 18.45 | 16.38
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3485 | 15.95 | 20.64 | 18.48
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 3271 | 18.23 | 21.66 | 19.56
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2926 | 17.79 | 26.61 | 25.09
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2845 | 20.57 | 25.01 | 22.57
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2443 | 25.69 | 26.40 | 26.19
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 2208 | 26.70 | 32.43 | 29.00
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1560 | 39.01 | 44.65 | 40.97


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22aiohttp-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3005%2C2118%2C1849%2C1654%2C1626%2C1461%2C1337%2C1272%2C1163%2C943%2C146%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 3005 | 19.40 | 22.48 | 21.28
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2118 | 28.58 | 31.18 | 30.21
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 1849 | 32.66 | 35.86 | 34.58
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 1654 | 36.99 | 39.76 | 38.65
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1626 | 38.09 | 40.86 | 39.34
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 1461 | 41.60 | 45.57 | 43.75
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1337 | 47.18 | 48.30 | 47.79
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1272 | 42.40 | 48.69 | 54.86
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 1163 | 46.71 | 60.57 | 56.18
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 943 | 64.27 | 69.05 | 67.73
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 146 | 419.29 | 430.60 | 431.99


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4325%2C3532%2C3461%2C3182%2C2791%2C2782%2C2623%2C2613%2C2155%2C1438%2C1231%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4325 | 13.40 | 17.13 | 14.82
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 3532 | 16.06 | 20.79 | 18.13
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3461 | 17.04 | 20.84 | 18.51
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3182 | 18.68 | 22.77 | 20.13
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2791 | 22.15 | 24.73 | 22.89
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2782 | 21.36 | 24.88 | 23.22
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2623 | 22.20 | 27.39 | 24.49
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2613 | 22.35 | 27.29 | 24.53
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2155 | 29.35 | 29.92 | 29.67
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1438 | 42.69 | 48.47 | 44.41
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1231 | 47.47 | 60.26 | 51.91


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4453%2C3988%2C3793%2C3757%2C3228%2C2970%2C2890%2C2797%2C2319%2C1993%2C1616%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 4453 | 12.98 | 16.80 | 14.41
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 3988 | 14.44 | 18.36 | 16.05
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3793 | 15.13 | 19.18 | 16.95
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 3757 | 15.34 | 19.55 | 17.07
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 3228 | 19.05 | 21.45 | 19.81
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2970 | 19.86 | 23.91 | 21.62
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2890 | 20.66 | 23.66 | 22.41
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2797 | 20.80 | 25.48 | 23.05
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 2319 | 26.89 | 27.82 | 27.57
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1993 | 29.39 | 35.08 | 32.09
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1616 | 38.09 | 43.24 | 39.55


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4396%2C2771%2C1949%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 4396 | 13.16 | 16.91 | 14.58
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2771 | 21.12 | 25.17 | 23.12
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1949 | 30.34 | 36.80 | 32.81


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B501%2C132%2C99%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 501 | 123.86 | 124.99 | 126.93
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 132 | 463.85 | 475.44 | 477.58
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 99 | 625.39 | 642.26 | 635.11


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2532%2C1281%2C969%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2532 | 22.72 | 29.17 | 25.28
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 1281 | 46.15 | 55.23 | 49.85
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 969 | 61.11 | 76.50 | 65.97


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4110%2C2986%2C1951%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 4110 | 13.80 | 18.01 | 15.58
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2986 | 19.91 | 24.09 | 21.44
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1951 | 30.39 | 36.37 | 32.78


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)