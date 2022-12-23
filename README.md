# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2022-12-23
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
* [The Results](#the-results-2022-12-23)
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

## The Results (2022-12-23)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3452%2C3277%2C3070%2C2874%2C2790%2C2646%2C2507%2C2184%2C1626%2C1444%2C1265%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 3452 | 17.78 | 20.31 | 18.63
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 3277 | 18.28 | 21.80 | 19.57
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 3070 | 19.11 | 24.03 | 20.87
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 2874 | 21.06 | 25.28 | 22.26
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 2790 | 21.23 | 26.39 | 22.98
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 2646 | 22.80 | 27.78 | 24.22
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 2507 | 24.34 | 29.87 | 25.49
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 2184 | 28.23 | 33.62 | 29.33
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1626 | 39.41 | 41.93 | 39.47
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.88.0` | 1444 | 43.17 | 50.23 | 44.27
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1265 | 48.17 | 55.04 | 50.49


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22emmett-raw%22%2C%22blacksheep-raw%22%2C%22baize-raw%22%2C%22starlette-raw%22%2C%22falcon-raw%22%2C%22sanic-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2015%2C1613%2C1408%2C1329%2C1213%2C1208%2C1144%2C1122%2C974%2C836%2C163%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2015 | 29.81 | 34.82 | 31.76
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 1613 | 37.35 | 44.84 | 39.61
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 1408 | 41.61 | 51.62 | 45.38
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 1329 | 44.49 | 55.41 | 48.11
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 1213 | 50.95 | 58.30 | 52.66
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 1208 | 49.17 | 61.78 | 53.01
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 1144 | 52.44 | 63.58 | 55.79
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 1122 | 52.34 | 64.31 | 57.11
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 974 | 65.66 | 68.36 | 65.56
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 836 | 74.46 | 83.64 | 76.36
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.88.0` | 163 | 380.03 | 419.94 | 388.69


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin-raw%22%2C%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2619%2C2420%2C2383%2C2360%2C2266%2C2127%2C1985%2C1952%2C1218%2C1170%2C1125%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2619 | 23.15 | 28.44 | 24.38
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 2420 | 25.18 | 30.72 | 26.40
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2383 | 25.45 | 30.80 | 26.87
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 2360 | 25.75 | 31.33 | 27.10
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 2266 | 27.73 | 32.36 | 28.17
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 2127 | 29.95 | 31.26 | 30.05
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 1985 | 30.44 | 36.84 | 32.48
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 1952 | 31.61 | 37.43 | 32.77
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1218 | 51.15 | 56.30 | 52.43
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1170 | 54.28 | 56.19 | 54.57
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.88.0` | 1125 | 56.18 | 64.09 | 56.81


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2932%2C2882%2C2723%2C2717%2C2455%2C2312%2C2139%2C1926%2C1338%2C1276%2C1240%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.3.0` | 2932 | 20.52 | 24.58 | 21.82
| [falcon-raw](https://pypi.org/project/falcon/) `3.1.0` | 2882 | 20.87 | 24.86 | 22.16
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.8` | 2723 | 21.64 | 27.25 | 23.48
| [muffin-raw](https://pypi.org/project/muffin/) `0.87.3` | 2717 | 21.93 | 27.17 | 23.51
| [baize-raw](https://pypi.org/project/baize/) `0.18.2` | 2455 | 25.78 | 27.16 | 26.03
| [emmett-raw](https://pypi.org/project/emmett/) `2.4.12` | 2312 | 25.86 | 31.99 | 27.81
| [starlette-raw](https://pypi.org/project/starlette/) `0.21.0` | 2139 | 28.98 | 34.71 | 29.87
| [sanic-raw](https://pypi.org/project/sanic/) `22.9.1` | 1926 | 31.64 | 38.10 | 33.17
| [quart-raw](https://pypi.org/project/quart/) `0.18.3` | 1338 | 46.29 | 53.68 | 47.74
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.3` | 1276 | 50.06 | 52.35 | 50.12
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.88.0` | 1240 | 49.52 | 59.69 | 51.55


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2847%2C2167%2C1208%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2847 | 20.85 | 26.05 | 22.49
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 2167 | 28.67 | 33.80 | 29.46
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.88.0` | 1208 | 51.41 | 60.98 | 52.88


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B992%2C106%2C73%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 992 | 60.53 | 74.10 | 64.40
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 106 | 558.72 | 700.65 | 593.48
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.88.0` | 73 | 788.09 | 917.51 | 844.82


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2365%2C914%2C629%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2365 | 26.29 | 31.16 | 27.00
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 914 | 70.06 | 79.26 | 69.85
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.88.0` | 629 | 102.62 | 115.72 | 101.41


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2766%2C1934%2C1418%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.3.0` | 2766 | 22.07 | 26.44 | 23.09
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.8` | 1934 | 31.92 | 37.81 | 33.04
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.88.0` | 1418 | 43.69 | 51.94 | 45.04


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)