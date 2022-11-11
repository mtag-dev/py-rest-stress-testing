# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-11-11
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
* [The Results](#the-results-2022-11-11)
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

## The Results (2022-11-11)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5317%2C5219%2C5217%2C5133%2C4820%2C4679%2C4529%2C3361%2C2647%2C2239%2C2154%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 5317 | 12.16 | 13.12 | 12.10
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 5219 | 12.34 | 13.34 | 12.40
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5217 | 12.25 | 13.28 | 12.40
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 5133 | 12.56 | 13.63 | 12.53
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 4820 | 13.96 | 14.67 | 13.30
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 4679 | 13.53 | 14.64 | 13.89
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 4529 | 14.26 | 15.46 | 14.13
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3361 | 18.05 | 20.73 | 19.16
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 2647 | 23.81 | 26.84 | 24.16
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 2239 | 28.31 | 28.57 | 28.56
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2154 | 28.09 | 30.63 | 29.68


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3412%2C2607%2C2339%2C1963%2C1901%2C1730%2C1684%2C1634%2C1260%2C1134%2C204%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3412 | 16.32 | 21.99 | 18.75
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2607 | 22.12 | 28.74 | 24.51
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 2339 | 24.60 | 31.66 | 27.32
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 1963 | 29.63 | 37.78 | 32.59
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 1901 | 30.68 | 40.48 | 33.66
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 1730 | 34.23 | 43.84 | 36.93
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 1684 | 34.63 | 45.60 | 37.93
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 1634 | 36.22 | 45.89 | 39.10
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1260 | 50.55 | 50.89 | 50.70
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1134 | 57.02 | 60.89 | 56.33
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 204 | 307.53 | 358.40 | 311.19


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4695%2C4596%2C4582%2C4296%2C3861%2C3682%2C3566%2C3154%2C1959%2C1755%2C1518%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4695 | 13.71 | 14.78 | 13.73
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 4596 | 14.04 | 15.23 | 13.95
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 4582 | 14.18 | 15.36 | 13.95
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 4296 | 15.08 | 16.25 | 14.93
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 3861 | 16.00 | 17.54 | 16.91
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 3682 | 17.24 | 18.57 | 17.34
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 3566 | 17.90 | 18.43 | 17.92
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3154 | 19.36 | 22.35 | 20.36
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1959 | 31.11 | 34.62 | 32.63
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1755 | 36.29 | 36.56 | 36.41
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 1518 | 41.96 | 47.52 | 42.07


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5143%2C4968%2C4966%2C4805%2C4217%2C4147%2C4052%2C3383%2C2274%2C2193%2C2181%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 5143 | 12.58 | 13.52 | 12.45
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 4968 | 13.03 | 13.99 | 12.92
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 4966 | 12.87 | 13.96 | 12.96
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4805 | 13.33 | 14.38 | 13.41
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 4217 | 15.09 | 15.53 | 15.15
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 4147 | 15.17 | 16.45 | 15.44
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 4052 | 15.18 | 16.59 | 16.23
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 3383 | 17.83 | 20.53 | 18.96
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.86.0` | 2274 | 27.43 | 31.12 | 28.10
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 2193 | 27.72 | 29.80 | 29.15
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 2181 | 29.09 | 29.43 | 29.33


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5006%2C3109%2C2042%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5006 | 12.84 | 13.91 | 12.87
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 3109 | 20.17 | 22.42 | 20.60
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 2042 | 31.10 | 34.68 | 31.29


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1406%2C152%2C84%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1406 | 42.04 | 53.90 | 45.40
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 152 | 409.93 | 482.96 | 415.23
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 84 | 719.62 | 889.62 | 739.38


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3980%2C1351%2C898%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 3980 | 16.10 | 17.25 | 16.07
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 1351 | 47.28 | 52.32 | 47.23
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 898 | 72.23 | 77.82 | 71.13


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4787%2C3730%2C2357%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4787 | 13.37 | 14.42 | 13.42
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 3730 | 16.74 | 18.16 | 17.16
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.86.0` | 2357 | 26.61 | 30.21 | 27.12


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)