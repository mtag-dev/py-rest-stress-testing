# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-07
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
* [The Results](#the-results-2021-11-07)
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * TODO: [POST: Create issue](#create-raw)
    * TODO: [PATCH: Update issue](#update-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * TODO: [POST: Create issue](#create-dataclass)
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

## The Results (2021-11-07)

### JSON response from primitives

<h3 id="userinfo-raw"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22muffin%22%2C%22falcon%22%2C%22blacksheep%22%2C%22blacksheep%22%2C%22falcon%22%2C%22baize%22%2C%22emmett%22%2C%22emmett%22%2C%22baize%22%2C%22starlette%22%2C%22starlette%22%2C%22squall%22%2C%22sanic%22%2C%22sanic%22%2C%22squall%22%2C%22fastapi%22%2C%22fastapi%22%2C%22quart%22%2C%22quart%22%2C%22aiohttp%22%2C%22aiohttp%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4553%2C4458%2C4392%2C4387%2C4374%2C4354%2C4170%2C4143%2C4085%2C4084%2C3991%2C3949%2C3780%2C3658%2C3644%2C3386%2C2874%2C2849%2C2049%2C2007%2C1800%2C1729%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 4553 | 6.50 | 7.72 | 7.07
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 4458 | 6.65 | 7.68 | 7.21
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 4392 | 6.73 | 7.98 | 7.32
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 4387 | 6.71 | 7.86 | 7.40
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 4374 | 6.73 | 8.11 | 7.38
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 4354 | 6.76 | 7.94 | 7.40
| [baize](https://pypi.org/project/baize/) `0.12.1` | 4170 | 7.05 | 8.66 | 7.71
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 4143 | 7.07 | 8.15 | 7.83
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 4085 | 7.14 | 8.48 | 7.97
| [baize](https://pypi.org/project/baize/) `0.12.1` | 4084 | 7.18 | 8.85 | 7.87
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3991 | 7.44 | 8.74 | 8.07
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3949 | 7.50 | 9.06 | 8.14
| [squall](https://pypi.org/project/squall/) `` | 3780 | 7.73 | 9.57 | 8.54
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3658 | 8.00 | 9.99 | 8.83
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3644 | 7.99 | 10.00 | 8.87
| [squall](https://pypi.org/project/squall/) `` | 3386 | 8.60 | 10.50 | 9.55
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2874 | 10.09 | 13.01 | 11.20
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2849 | 10.15 | 12.80 | 11.27
| [quart](https://pypi.org/project/quart/) `0.15.1` | 2049 | 15.28 | 16.87 | 15.68
| [quart](https://pypi.org/project/quart/) `0.15.1` | 2007 | 15.52 | 16.88 | 16.13
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1800 | 17.58 | 18.13 | 17.83
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1729 | 17.93 | 18.67 | 18.52


</details>


<h3 id="sprint-raw"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22muffin%22%2C%22emmett%22%2C%22emmett%22%2C%22squall%22%2C%22squall%22%2C%22falcon%22%2C%22falcon%22%2C%22sanic%22%2C%22sanic%22%2C%22blacksheep%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22baize%22%2C%22starlette%22%2C%22aiohttp%22%2C%22aiohttp%22%2C%22quart%22%2C%22quart%22%2C%22fastapi%22%2C%22fastapi%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3595%2C3475%2C3193%2C3188%2C3051%2C2727%2C2057%2C2036%2C1973%2C1951%2C1895%2C1853%2C1834%2C1810%2C1788%2C1763%2C1237%2C1235%2C1227%2C1220%2C204%2C204%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3595 | 8.32 | 9.13 | 8.93
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3475 | 8.40 | 9.59 | 9.34
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 3193 | 9.27 | 9.98 | 10.10
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 3188 | 9.32 | 10.09 | 10.13
| [squall](https://pypi.org/project/squall/) `` | 3051 | 9.70 | 10.89 | 10.53
| [squall](https://pypi.org/project/squall/) `` | 2727 | 10.96 | 11.74 | 11.76
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 2057 | 14.28 | 16.24 | 15.55
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 2036 | 14.50 | 15.86 | 15.73
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1973 | 14.90 | 16.95 | 16.26
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1951 | 14.99 | 16.95 | 16.46
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 1895 | 15.53 | 17.29 | 16.91
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 1853 | 15.84 | 17.78 | 17.27
| [baize](https://pypi.org/project/baize/) `0.12.1` | 1834 | 16.05 | 17.75 | 17.45
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1810 | 16.23 | 17.96 | 17.68
| [baize](https://pypi.org/project/baize/) `0.12.1` | 1788 | 16.43 | 18.47 | 17.93
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1763 | 17.00 | 18.11 | 18.20
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1237 | 25.57 | 26.19 | 25.87
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1235 | 25.70 | 26.39 | 25.92
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1227 | 24.34 | 27.50 | 26.11
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1220 | 24.36 | 27.62 | 26.23
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 204 | 145.35 | 160.57 | 156.49
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 204 | 151.25 | 157.11 | 156.74


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22blacksheep-dataclass%22%2C%22squall-dataclass%22%2C%22squall-dataclass%22%2C%22fastapi-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3862%2C3844%2C3292%2C2894%2C2540%2C2531%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3862 | 7.65 | 9.28 | 8.32
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3844 | 7.56 | 9.70 | 8.35
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 3292 | 8.79 | 11.05 | 9.82
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 2894 | 9.89 | 12.60 | 11.19
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2540 | 11.69 | 13.43 | 12.66
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2531 | 11.38 | 14.69 | 12.71


</details>


<h3 id="sprint-dataclass"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclass%22%2C%22squall-dataclass%22%2C%22blacksheep-dataclass%22%2C%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B361%2C360%2C215%2C214%2C136%2C134%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 361 | 85.77 | 88.45 | 88.55
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 360 | 85.19 | 87.71 | 88.70
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 215 | 138.58 | 148.09 | 147.61
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 214 | 139.43 | 147.74 | 148.78
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 136 | 225.08 | 236.43 | 236.29
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 134 | 224.49 | 235.90 | 237.08


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3366%2C3338%2C3292%2C2910%2C2167%2C2144%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 3366 | 8.63 | 10.92 | 9.56
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 3338 | 8.84 | 10.57 | 9.64
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 3292 | 8.91 | 11.10 | 9.79
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2910 | 10.03 | 11.58 | 11.06
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2167 | 13.37 | 16.76 | 14.82
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2144 | 13.30 | 17.02 | 14.96


</details>


<h3 id="sprint-pydantic"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B333%2C321%2C193%2C193%2C89%2C87%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 333 | 92.67 | 95.72 | 96.00
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 321 | 95.54 | 98.16 | 99.47
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 193 | 156.65 | 166.11 | 165.94
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 193 | 156.62 | 166.49 | 165.49
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 89 | 332.04 | 358.42 | 357.40
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 87 | 338.32 | 357.78 | 361.89


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)