# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-01-18
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
* [The Results](#the-results-2022-01-18)
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

## The Results (2022-01-18)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5420%2C5378%2C5361%2C5107%2C4777%2C4718%2C4702%2C3912%2C3023%2C2155%2C2139%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5420 | 11.63 | 13.56 | 11.86
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 5378 | 11.91 | 13.18 | 12.04
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5361 | 11.75 | 13.42 | 12.01
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5107 | 12.46 | 13.95 | 12.70
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 4777 | 13.09 | 15.12 | 13.64
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4718 | 13.71 | 14.93 | 13.57
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4702 | 13.38 | 15.17 | 13.62
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3912 | 15.80 | 17.68 | 16.53
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 3023 | 19.96 | 23.53 | 21.22
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2155 | 29.77 | 30.10 | 29.72
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2139 | 28.11 | 31.48 | 29.88


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3725%2C2752%2C2169%2C2124%2C1870%2C1738%2C1622%2C1618%2C1224%2C1122%2C231%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3725 | 16.55 | 18.97 | 17.20
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2752 | 22.04 | 26.95 | 23.21
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 2169 | 27.56 | 33.96 | 29.47
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 2124 | 28.55 | 34.60 | 30.10
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1870 | 31.96 | 40.42 | 34.16
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1738 | 34.12 | 42.57 | 36.77
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1622 | 37.62 | 46.11 | 39.39
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1618 | 37.08 | 46.98 | 39.49
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1224 | 51.92 | 52.28 | 52.21
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1122 | 56.09 | 62.16 | 56.94
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 231 | 251.62 | 332.69 | 275.62


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4773%2C4708%2C4639%2C4347%2C4010%2C3821%2C3630%2C3417%2C1930%2C1925%2C1694%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4773 | 13.27 | 14.88 | 13.51
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4708 | 13.54 | 15.15 | 13.61
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4639 | 13.86 | 15.44 | 13.77
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4347 | 14.66 | 16.37 | 14.82
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 4010 | 15.16 | 17.09 | 16.35
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3821 | 16.40 | 18.36 | 16.71
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3630 | 17.38 | 18.70 | 17.60
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3417 | 17.54 | 20.61 | 18.87
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1930 | 33.22 | 33.52 | 33.18
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1925 | 31.15 | 35.97 | 33.20
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1694 | 36.16 | 43.39 | 37.70


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22squall-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5278%2C5171%2C5100%2C4908%2C4386%2C4330%2C4198%2C3608%2C2511%2C2364%2C2188%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5278 | 12.13 | 13.34 | 12.12
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5171 | 12.26 | 13.77 | 12.43
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5100 | 12.36 | 13.79 | 12.70
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 4908 | 12.85 | 14.44 | 13.16
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4386 | 14.33 | 16.04 | 14.59
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4330 | 14.49 | 15.79 | 14.76
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.0` | 4198 | 14.39 | 16.32 | 15.66
| [sanic-raw](https://pypi.org/project/sanic/) `21.12.1` | 3608 | 16.55 | 19.22 | 17.96
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2511 | 24.42 | 28.90 | 25.47
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2364 | 26.74 | 27.29 | 27.06
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2188 | 27.39 | 30.78 | 29.20


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5119%2C3539%2C2520%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 5119 | 12.37 | 13.87 | 12.63
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3539 | 17.29 | 19.71 | 18.08
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2520 | 24.64 | 28.14 | 25.34


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B1501%2C196%2C144%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 1501 | 42.36 | 48.47 | 42.54
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 196 | 326.38 | 362.42 | 323.83
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 144 | 439.30 | 504.31 | 432.15


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4134%2C1669%2C1277%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4134 | 15.30 | 17.04 | 15.51
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1669 | 38.25 | 42.63 | 38.29
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1277 | 49.02 | 55.79 | 50.02


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4976%2C3981%2C2489%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 4976 | 12.78 | 14.19 | 12.94
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3981 | 15.69 | 17.43 | 16.07
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2489 | 24.85 | 29.17 | 25.67


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)