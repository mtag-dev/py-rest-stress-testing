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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3437%2C3279%2C3089%2C2967%2C2824%2C2590%2C2566%2C2217%2C1821%2C1508%2C1314%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 3437 | 17.87 | 20.52 | 18.67
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 3279 | 18.67 | 21.68 | 19.49
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 3089 | 19.50 | 23.41 | 20.74
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2967 | 20.34 | 24.86 | 21.56
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2824 | 21.46 | 26.15 | 22.63
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2590 | 23.26 | 28.40 | 24.71
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2566 | 23.93 | 28.70 | 24.93
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2217 | 28.00 | 33.06 | 28.82
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1821 | 34.30 | 40.20 | 35.10
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1508 | 41.31 | 43.25 | 42.39
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1314 | 47.85 | 52.72 | 48.59


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2412%2C1846%2C1493%2C1384%2C1325%2C1241%2C1216%2C1174%2C964%2C781%2C175%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 2412 | 25.48 | 30.24 | 26.48
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 1846 | 33.80 | 39.66 | 34.62
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 1493 | 39.59 | 49.88 | 42.78
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 1384 | 43.42 | 53.63 | 46.17
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1325 | 45.18 | 56.21 | 48.21
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 1241 | 47.87 | 60.50 | 51.45
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 1216 | 50.06 | 60.55 | 52.56
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 1174 | 51.39 | 63.31 | 54.38
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 964 | 65.70 | 67.62 | 66.25
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 781 | 81.07 | 89.27 | 81.72
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 175 | 357.45 | 382.75 | 361.24


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2864%2C2580%2C2542%2C2415%2C2412%2C2221%2C2181%2C1978%2C1407%2C1218%2C1150%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 2864 | 20.97 | 25.55 | 22.29
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2580 | 23.55 | 28.67 | 24.75
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2542 | 23.68 | 29.26 | 25.12
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 2415 | 25.55 | 30.57 | 26.44
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2412 | 26.47 | 27.73 | 26.49
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2221 | 27.09 | 33.27 | 28.80
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2181 | 28.36 | 34.11 | 29.27
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 1978 | 30.98 | 37.24 | 32.29
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1407 | 44.94 | 46.23 | 45.43
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1218 | 51.61 | 56.82 | 52.45
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1150 | 54.65 | 62.97 | 55.51


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2970%2C2942%2C2916%2C2804%2C2737%2C2402%2C2291%2C2095%2C1680%2C1615%2C1363%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.1.1` | 2970 | 20.19 | 24.72 | 21.50
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.0` | 2942 | 20.31 | 24.83 | 21.75
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 2916 | 20.60 | 25.32 | 21.89
| [baize-raw](https://pypi.org/project/baize/) `0.12.1` | 2804 | 22.62 | 23.79 | 22.79
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.0` | 2737 | 21.73 | 27.40 | 23.36
| [starlette-raw](https://pypi.org/project/starlette/) `0.16.0` | 2402 | 25.28 | 31.07 | 26.58
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2291 | 26.05 | 32.22 | 27.87
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.1` | 2095 | 29.09 | 35.46 | 30.51
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.0` | 1680 | 37.53 | 38.81 | 38.08
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.0` | 1615 | 38.16 | 45.37 | 39.55
| [quart-raw](https://pypi.org/project/quart/) `0.15.1` | 1363 | 46.01 | 50.74 | 46.90


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2971%2C2205%2C1577%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2971 | 20.37 | 24.54 | 21.51
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2205 | 28.66 | 32.77 | 28.96
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1577 | 39.81 | 46.18 | 40.51


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B610%2C148%2C114%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 610 | 98.64 | 120.60 | 104.38
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 148 | 415.65 | 516.08 | 427.70
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 114 | 551.73 | 640.13 | 550.39


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2055%2C1082%2C882%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2055 | 30.34 | 35.33 | 31.07
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 1082 | 58.98 | 66.94 | 58.99
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 882 | 73.42 | 81.65 | 72.35


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2886%2C2211%2C1532%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.1.1` | 2886 | 20.96 | 25.58 | 22.12
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.0` | 2211 | 27.78 | 33.44 | 28.84
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.0` | 1532 | 40.20 | 48.04 | 41.70


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)