# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-04
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
* [The Results](#the-results-2021-11-04)
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

## The Results (2021-11-04)

### JSON response from primitives

<h3 id="userinfo-raw"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22falcon%22%2C%22blacksheep%22%2C%22emmett%22%2C%22baize%22%2C%22starlette%22%2C%22sanic%22%2C%22squall%22%2C%22fastapi%22%2C%22quart%22%2C%22aiohttp%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3787%2C3727%2C3448%2C3418%2C3385%2C3314%2C3024%2C2566%2C2537%2C1767%2C1327%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3787 | 7.85 | 9.21 | 8.64
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 3727 | 8.02 | 9.34 | 8.72
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 3448 | 8.45 | 10.12 | 9.62
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 3418 | 8.74 | 10.09 | 9.50
| [baize](https://pypi.org/project/baize/) `0.12.1` | 3385 | 8.96 | 10.37 | 9.52
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3314 | 9.15 | 10.49 | 9.69
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3024 | 10.02 | 11.41 | 10.70
| [squall](https://pypi.org/project/squall/) `` | 2566 | 11.31 | 13.69 | 12.78
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2537 | 12.19 | 13.46 | 12.62
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1767 | 13.09 | 25.17 | 28.99
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1327 | 13.66 | 48.90 | 54.02


</details>


<h3 id="sprint-raw"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22emmett%22%2C%22squall%22%2C%22falcon%22%2C%22sanic%22%2C%22blacksheep%22%2C%22starlette%22%2C%22baize%22%2C%22quart%22%2C%22aiohttp%22%2C%22fastapi%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3031%2C2693%2C2547%2C1871%2C1800%2C1678%2C1670%2C1661%2C1109%2C1106%2C195%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3031 | 9.99 | 11.46 | 10.60
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 2693 | 11.31 | 12.85 | 11.93
| [squall](https://pypi.org/project/squall/) `` | 2547 | 12.29 | 13.42 | 12.62
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 1871 | 16.50 | 18.14 | 17.10
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1800 | 17.16 | 18.80 | 17.78
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 1678 | 18.43 | 20.24 | 19.09
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1670 | 18.40 | 20.55 | 19.16
| [baize](https://pypi.org/project/baize/) `0.12.1` | 1661 | 18.60 | 20.56 | 19.27
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1109 | 21.36 | 40.94 | 33.68
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1106 | 17.95 | 51.23 | 33.71
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 195 | 157.81 | 172.88 | 163.67


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22squall-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3310%2C2800%2C2325%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3310 | 9.25 | 10.29 | 9.70
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 2800 | 11.08 | 12.22 | 11.45
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2325 | 13.46 | 14.70 | 13.79


</details>


<h3 id="sprint-dataclass"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclass%22%2C%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B344%2C211%2C130%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 344 | 89.22 | 100.43 | 92.94
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 211 | 144.25 | 163.06 | 151.06
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 130 | 239.96 | 264.32 | 244.42


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3001%2C2694%2C2121%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 3001 | 10.25 | 11.37 | 10.70
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2694 | 11.57 | 12.66 | 11.90
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2121 | 14.72 | 16.11 | 15.12


</details>


<h3 id="sprint-pydantic"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B323%2C191%2C87%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 323 | 94.61 | 104.91 | 98.83
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 191 | 165.69 | 180.67 | 166.93
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 87 | 352.90 | 394.83 | 364.11


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)