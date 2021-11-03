# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-03
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
* [The Results](#the-results-2021-11-03)
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

## The Results (2021-11-03)

### JSON response from primitives

<h3 id="userinfo-raw"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22blacksheep%22%2C%22falcon%22%2C%22emmett%22%2C%22starlette%22%2C%22baize%22%2C%22sanic%22%2C%22fastapi%22%2C%22aiohttp%22%2C%22quart%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4536%2C4326%2C4198%2C3927%2C3748%2C3736%2C3150%2C2606%2C1980%2C1801%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 4536 | 13.88 | 14.73 | 14.11
| [blacksheep](https://pypi.org/project/blacksheep/) `1.0.9` | 4326 | 14.69 | 15.57 | 14.85
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 4198 | 15.10 | 15.84 | 15.25
| [emmett](https://pypi.org/project/emmett/) `2.3.1` | 3927 | 16.14 | 16.90 | 16.32
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3748 | 16.76 | 17.63 | 17.06
| [baize](https://pypi.org/project/baize/) `0.12` | 3736 | 16.73 | 17.47 | 17.12
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3150 | 19.74 | 20.89 | 20.36
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2606 | 24.16 | 25.30 | 24.57
| [aiohttp](https://pypi.org/project/aiohttp/) `3.7.4.post0` | 1980 | 8.39 | 128.81 | 103.17
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1801 | 16.55 | 60.80 | 65.18


</details>


<h3 id="sprint-raw"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22emmett%22%2C%22sanic%22%2C%22falcon%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22aiohttp%22%2C%22quart%22%2C%22fastapi%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3189%2C2840%2C1804%2C1664%2C1494%2C1471%2C1454%2C1155%2C1006%2C206%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3189 | 19.73 | 20.48 | 20.08
| [emmett](https://pypi.org/project/emmett/) `2.3.1` | 2840 | 22.19 | 23.19 | 22.53
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1804 | 33.58 | 36.09 | 35.46
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 1664 | 37.05 | 39.21 | 38.42
| [blacksheep](https://pypi.org/project/blacksheep/) `1.0.9` | 1494 | 42.11 | 44.11 | 42.96
| [baize](https://pypi.org/project/baize/) `0.12` | 1471 | 42.72 | 44.71 | 43.47
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1454 | 43.84 | 45.62 | 44.06
| [aiohttp](https://pypi.org/project/aiohttp/) `3.7.4.post0` | 1155 | 14.50 | 15.95 | 27.19
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1006 | 37.08 | 107.30 | 119.20
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 206 | 302.35 | 313.85 | 307.02


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3476%2C2224%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3476 | 18.11 | 19.00 | 18.41
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2224 | 28.50 | 29.57 | 28.78


</details>


<h3 id="sprint-dataclass"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B212%2C126%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 212 | 296.78 | 317.14 | 299.35
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 126 | 484.17 | 540.54 | 500.16


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B2956%2C2055%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 2956 | 21.20 | 22.46 | 21.73
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2055 | 30.75 | 32.18 | 31.24


</details>


<h3 id="sprint-pydantic"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B166%2C83%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 166 | 374.23 | 405.92 | 380.48
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 83 | 771.12 | 795.84 | 757.40


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)