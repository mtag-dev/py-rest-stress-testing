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



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22falcon%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22sanic%22%2C%22squall%22%2C%22emmett%22%2C%22fastapi%22%2C%22quart%22%2C%22aiohttp%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4533%2C4413%2C4366%2C4092%2C3941%2C3587%2C3396%2C3301%2C2855%2C2005%2C1723%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 4533 | 6.54 | 7.58 | 7.11
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 4413 | 6.72 | 7.61 | 7.31
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 4366 | 6.84 | 7.79 | 7.40
| [baize](https://pypi.org/project/baize/) `0.12.1` | 4092 | 7.22 | 8.71 | 7.83
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3941 | 7.49 | 8.98 | 8.13
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3587 | 8.17 | 9.98 | 8.99
| [squall](https://pypi.org/project/squall/) `` | 3396 | 8.59 | 10.68 | 9.50
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 3301 | 8.46 | 11.05 | 10.02
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2855 | 10.20 | 12.99 | 11.23
| [quart](https://pypi.org/project/quart/) `0.15.1` | 2005 | 15.44 | 16.99 | 15.97
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1723 | 17.54 | 18.37 | 18.64


</details>


<h3 id="sprint-raw"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22emmett%22%2C%22squall%22%2C%22falcon%22%2C%22sanic%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22quart%22%2C%22aiohttp%22%2C%22fastapi%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3400%2C3154%2C2771%2C2080%2C1950%2C1875%2C1807%2C1769%2C1217%2C1216%2C204%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3400 | 8.55 | 10.42 | 9.47
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 3154 | 9.38 | 10.17 | 10.30
| [squall](https://pypi.org/project/squall/) `` | 2771 | 10.75 | 11.80 | 11.60
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 2080 | 14.13 | 16.03 | 15.37
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1950 | 15.04 | 17.45 | 16.43
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 1875 | 15.50 | 17.77 | 17.08
| [baize](https://pypi.org/project/baize/) `0.12.1` | 1807 | 16.35 | 17.80 | 17.73
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1769 | 16.62 | 18.47 | 18.10
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1217 | 24.38 | 27.76 | 26.28
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1216 | 25.60 | 26.26 | 26.30
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 204 | 149.64 | 158.42 | 156.27


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22squall-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3794%2C3051%2C2520%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3794 | 7.83 | 9.28 | 8.46
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 3051 | 9.50 | 12.26 | 10.58
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2520 | 11.51 | 14.60 | 12.79


</details>


<h3 id="sprint-dataclass"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclass%22%2C%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B349%2C216%2C135%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 349 | 87.91 | 90.77 | 91.89
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 216 | 137.97 | 147.20 | 147.93
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 135 | 231.17 | 239.97 | 236.79


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3410%2C2989%2C2196%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 3410 | 8.56 | 10.90 | 9.43
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2989 | 9.72 | 12.27 | 10.80
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2196 | 13.10 | 16.69 | 14.61


</details>


<h3 id="sprint-pydantic"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B334%2C196%2C86%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 334 | 92.20 | 96.37 | 95.67
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 196 | 152.11 | 160.41 | 162.89
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 86 | 342.72 | 422.32 | 368.22


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)