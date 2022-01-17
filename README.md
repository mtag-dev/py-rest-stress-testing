# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-01-17
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
* [The Results](#the-results-2022-01-17)
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

## The Results (2022-01-17)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5180%2C5148%2C5077%2C5071%2C4719%2C4528%2C4443%2C3533%2C2823%2C2143%2C1990%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5180 | 12.39 | 13.50 | 12.56
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5148 | 12.53 | 13.66 | 12.51
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5077 | 12.85 | 13.87 | 12.68
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5071 | 12.56 | 13.70 | 12.87
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4719 | 13.83 | 14.97 | 13.60
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4528 | 14.12 | 15.51 | 14.43
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4443 | 14.58 | 15.73 | 14.42
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3533 | 17.48 | 19.24 | 18.25
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2823 | 22.40 | 24.98 | 22.71
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2143 | 29.53 | 29.78 | 29.83
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1990 | 30.76 | 33.26 | 32.13


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3382%2C2640%2C2104%2C2037%2C1820%2C1646%2C1619%2C1603%2C1214%2C1069%2C220%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3382 | 17.25 | 21.64 | 18.95
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2640 | 22.29 | 27.89 | 24.21
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2104 | 27.61 | 35.26 | 30.38
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2037 | 29.26 | 35.98 | 31.39
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1820 | 32.42 | 41.45 | 35.11
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1646 | 36.15 | 45.62 | 38.79
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1619 | 37.52 | 46.04 | 39.43
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1603 | 38.10 | 45.96 | 39.86
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1214 | 52.43 | 52.84 | 52.63
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1069 | 60.59 | 64.66 | 59.77
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 220 | 284.67 | 345.07 | 289.52


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4601%2C4581%2C4492%2C4215%2C3698%2C3598%2C3487%2C3210%2C1874%2C1801%2C1588%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4601 | 13.91 | 15.08 | 14.07
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4581 | 14.29 | 15.40 | 14.01
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4492 | 14.59 | 15.77 | 14.23
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4215 | 15.36 | 16.56 | 15.32
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3698 | 16.66 | 18.13 | 17.77
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3598 | 17.63 | 19.01 | 17.76
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3487 | 18.31 | 18.88 | 18.32
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3210 | 18.89 | 21.81 | 20.10
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1874 | 33.94 | 34.34 | 34.13
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1801 | 33.86 | 37.93 | 35.47
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1588 | 39.46 | 44.94 | 40.16


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5057%2C4864%2C4863%2C4700%2C4087%2C4068%2C3907%2C3380%2C2395%2C2383%2C2056%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5057 | 12.84 | 13.82 | 12.67
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4864 | 13.25 | 14.32 | 13.21
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4863 | 13.19 | 14.21 | 13.32
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4700 | 13.51 | 14.74 | 13.79
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4087 | 15.60 | 16.91 | 15.66
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4068 | 15.68 | 16.16 | 15.71
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3907 | 15.88 | 17.25 | 16.91
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3380 | 17.86 | 20.70 | 19.11
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2395 | 25.71 | 30.06 | 26.69
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2383 | 26.62 | 27.03 | 26.84
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2056 | 29.36 | 32.67 | 31.08


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4926%2C3465%2C2426%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4926 | 13.05 | 14.18 | 13.14
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3465 | 18.22 | 19.52 | 18.48
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2426 | 26.21 | 28.69 | 26.35


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1392%2C179%2C140%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1392 | 43.65 | 53.94 | 45.98
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 179 | 345.73 | 408.28 | 351.05
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 140 | 448.50 | 525.08 | 450.95


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3886%2C1588%2C1182%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 3886 | 16.55 | 17.72 | 16.49
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1588 | 40.66 | 43.70 | 40.20
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1182 | 53.90 | 59.90 | 54.03


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4713%2C3733%2C2291%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4713 | 13.64 | 14.81 | 13.68
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3733 | 16.82 | 18.27 | 17.16
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2291 | 26.88 | 31.11 | 27.89


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)